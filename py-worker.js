// Runs candidate Python in Pyodide, off the main thread so a runaway loop can be killed.
let py = null;
let booting = null;

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

function cleanTrace(msg) {
  const lines = String(msg || "").split("\n");
  const i = lines.findIndex(l => l.includes('File "<exec>"'));
  return (i > 0 ? ["Traceback (most recent call last):", ...lines.slice(i)] : lines).join("\n").trim();
}

self.onmessage = async (e) => {
  const { id, type, code, tests, indexURL } = e.data;
  try {
    await boot(indexURL);
    if (type === "boot") { self.postMessage({ id, ok: true, ready: true }); return; }

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
    if (!error && Array.isArray(tests) && tests.length) {
      const runTests = py.globals.get("__run_tests");
      const pyTests = py.toPy(tests);
      const res = runTests(pyTests, ns);
      results = res.toJs({ dict_converter: Object.fromEntries });
      res.destroy(); pyTests.destroy(); runTests.destroy();
    }
    ns.destroy();
    self.postMessage({ id, ok: true, stdout: out.join("\n"), error, results, ms: Math.round(performance.now() - t0) });
  } catch (err) {
    self.postMessage({ id, ok: false, fatal: true, error: String((err && err.message) || err) });
  }
};
