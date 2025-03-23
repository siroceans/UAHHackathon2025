import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

// Create scene
const scene = new THREE.Scene();
scene.background = new THREE.Color(0xffffff);

// Create camera
const camera = new THREE.PerspectiveCamera(
    75,
    window.innerWidth / window.innerHeight,
    0.1,
    1000
);
camera.position.set = (5, 2, 10);

// Create renderer
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Add 
const ambient = new THREE.AmbientLight(0xffffff, 5);
scene.add(ambient);

const directional = new THREE.DirectionalLight(0xffffff, 5);
directional.position.set(5, 10, 5);
scene.add(directional);

let model = null;

// Load model
const loader = new GLTFLoader();
const modelPath = document.getElementById("model-path").getAttribute("data-path");

loader.load(modelPath, (gltf) => {
    const model = gltf.scene;
    model.scale.set(0.5, 0.5, 0.5);
    model.position.set(0, 0, 0);
    model.rotation.y = Math.PI;
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
