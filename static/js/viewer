// viewer.js
import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js';
import { GLTFLoader } from 'https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/loaders/GLTFLoader.js';

// Create scene
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x111111);

// Create camera
const camera = new THREE.PerspectiveCamera(
    75,
    window.innerWidth / window.innerHeight,
    0.1,
    1000
);
camera.position.z = 5;

// Create renderer
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Add light
const light = new THREE.HemisphereLight(0xffffff, 0x444444);
scene.add(light);

// Load model
const loader = new GLTFLoader();
const modelPath = document.getElementById("model-path").getAttribute("data-path");

loader.load(modelPath, (gltf) => {
    const model = gltf.scene;
    model.position.set(0, 0, 0);
    scene.add(model);
}, undefined, (error) => {
    console.error("Error loading model:", error);
});

// Animate
function animate() {
    requestAnimationFrame(animate);

    if (model) {
        modelPath.rotation.y += 0.01;
    }

    renderer.render(scene, camera);
}
animate();
