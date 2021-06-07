// const Module = require("../../backend/wasm/build/search");
// const Module = require("../../^untitled:Untitled-2");


function* performSearch(query) {
    // Module.asm = asm;
    // initRuntime();
    // console.log(asm);
    // createWasm();

    var search = Module.cwrap('performSearch', null, ['string']);
    var getres = Module.cwrap('getSearch', 'string');
    search(query);

    while (result = getres()) {
        yield result;
    }
}

// function* performSearch2(query) {
//     var importObject = {
//         imports: { imported_func: arg => console.log(arg) }
//       };

//     WebAssembly.instantiateStreaming(fetch('simple.wasm'), importObject)
//     .then(obj => obj.instance.exports.exported_func());
// }