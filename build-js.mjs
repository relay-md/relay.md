import * as esbuild from 'esbuild'

const config = {
    entryPoints: ['backend/static/es/main.js'],
    outdir: 'backend/static/js',
    bundle: true,
    minify: true,
    plugins: [],
    sourcemap: true,
}
function success() {
    console.log('Bundling successful!');
}

function error(msg) {
    console.error('Bundling failed:', msg);
}

await esbuild.build(config)
    .then(success)
    .catch(error);
