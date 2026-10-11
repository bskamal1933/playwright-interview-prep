// Runs candidate Python in Pyodide, off the main thread so a runaway loop can be killed.
let py = null;
let booting = null;
let requestsReady = null;

const HARNESS = `
import ast

def __run_tests(tests, ns):
    results = []
    for t in tests:
        try:
            exec(compile(t, "<test>", "exec"), ns)
            results.append({"test": t, "ok": True})
        except AssertionError as e:
            got = None
            try:
                node = ast.parse(t).body[0]
                if isinstance(node, ast.Assert) and isinstance(node.test, ast.Compare):
                    got = repr(eval(compile(ast.Expression(node.test.left), "<got>", "eval"), ns))
            except Exception:
                pass
            results.append({"test": t, "ok": False, "got": got, "err": str(e)})
        except Exception as e:
            results.append({"test": t, "ok": False, "err": f"{type(e).__name__}: {e}"})
    return results
`;

// Pure-Python wheels for requests, self-hosted (named .wasm so every static host serves them).
const WHEELS = ["urllib3-2.2.3", "idna-3.10", "certifi-2024.8.30", "charset_normalizer-3.4.0", "requests-2.32.3"];

function boot(indexURL) {
  if (!booting) {
    booting = (async () => {
      importScripts(indexURL + "pyodide.js");
      py = await self.loadPyodide({ indexURL, stdLibURL: indexURL + "python_stdlib.wasm" });
      py.runPython(HARNESS);
      py.setStdin({ error: true });
    })();
  }
  return booting;
}

async function fetchBytes(url) {
  const r = await fetch(url);
  if (!r.ok) throw new Error(`Couldn't load ${url} (${r.status})`);
  return r.arrayBuffer();
}

function ensureRequests(assetBase) {
  if (!requestsReady) {
    requestsReady = (async () => {
      const site = py.runPython("import site; site.getsitepackages()[0]");
      for (const w of WHEELS) {
        const buf = await fetchBytes(`${assetBase}pywheels/${w}-py3-none-any.whl.wasm`);
        py.unpackArchive(buf, "wheel", { extractDir: site });
      }
      const harness = await (await fetch(`${assetBase}pyharness/apisim.py`)).text();
      py.FS.writeFile("/home/pyodide/apisim.py", harness);
      const data = new Uint8Array(await fetchBytes(`${assetBase}pyharness/jsonplaceholder.json`));
      py.FS.writeFile("/home/pyodide/jsonplaceholder.json", data);
      py.runPython(`
import sys
if "/home/pyodide" not in sys.path:
    sys.path.insert(0, "/home/pyodide")
import apisim
apisim.load_jsonplaceholder("/home/pyodide/jsonplaceholder.json")
`);
    })().catch(err => { requestsReady = null; throw err; });
  }
  return requestsReady;
}

function cleanTrace(msg) {
  const lines = String(msg || "").split("\n");
  const i = lines.findIndex(l => l.includes('File "<exec>"'));
  return (i > 0 ? ["Traceback (most recent call last):", ...lines.slice(i)] : lines).join("\n").trim();
}

self.onmessage = async (e) => {
  const { id, type, code, tests, indexURL, assetBase, api } = e.data;
  try {
    await boot(indexURL);
    if (type === "boot") { self.postMessage({ id, ok: true, ready: true }); return; }

    const needsRequests = !!api || /\b(import|from)\s+requests\b/.test(code || "");
    if (needsRequests) await ensureRequests(assetBase);

    const out = [];
    py.setStdout({ batched: s => out.push(s) });
    py.setStderr({ batched: s => out.push(s) });

    const ns = py.globals.get("dict")();
    const t0 = performance.now();
    let error = null;
    try {
      await py.runPythonAsync(code, { globals: ns });
    } catch (err) {
      error = cleanTrace(err && err.message);
    }

    let results = [];
    let mode = null;
    if (!error && api) {
      const run = py.pyimport("apisim").run_api_task;
      const res = run(ns, py.toPy(tests || []), api.entry || null, py.toPy(api.mutants || []), api.live !== false);
      const js = res.toJs({ dict_converter: Object.fromEntries });
      results = js.results; mode = js.mode;
      res.destroy(); run.destroy();
    } else if (!error && Array.isArray(tests) && tests.length) {
      const runTests = py.globals.get("__run_tests");
      const pyTests = py.toPy(tests);
      const res = runTests(pyTests, ns);
      results = res.toJs({ dict_converter: Object.fromEntries });
      res.destroy(); pyTests.destroy(); runTests.destroy();
    }
    ns.destroy();
    self.postMessage({ id, ok: true, stdout: out.join("\n"), error, results, mode, ms: Math.round(performance.now() - t0) });
  } catch (err) {
    self.postMessage({ id, ok: false, fatal: true, error: String((err && err.message) || err) });
  }
};
