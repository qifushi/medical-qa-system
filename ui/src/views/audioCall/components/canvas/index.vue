<template>
  <div ref="canvasContainer" class="canvas-container">
  </div>
</template>

<script setup>
import reglLib from 'regl'
import { defineProps, onMounted, ref } from 'vue'
const props = defineProps({
  speed: {
    type: Number,
    default: 1.0 // 默认速度
  },
  color: {
    type: Array,
    default: () => [0.5, 0.5, 1.0] // 默认颜色 [R, G, B]
  }
})
function Vector2(x = 0, y = 0) {
  this.x = x
  this.y = y
}

Object.defineProperties(Vector2.prototype, {
  width: {
    get() {
      return this.x
    },
    set(value) {
      this.x = value
    }
  },
  height: {
    get() {
      return this.y
    },
    set(value) {
      this.y = value
    }
  }
})

Object.assign(Vector2.prototype, {
  set(x, y) {
    this.x = x
    this.y = y
    return this
  },
  clone() {
    return new this.constructor(this.x, this.y)
  },
  add(v) {
    this.x += v.x
    this.y += v.y
    return this
  },
  sub(v) {
    this.x -= v.x
    this.y -= v.y
    return this
  },
  multiplyScalar(scalar) {
    this.x *= scalar
    this.y *= scalar
    return this
  },
  length() {
    return Math.sqrt(this.x * this.x + this.y * this.y)
  },
  normalize() {
    return this.multiplyScalar(1 / (this.length() || 1))
  }
})

const canvasContainer = ref(null)

onMounted(() => {
  // 创建 canvas 并添加到 canvasContainer
  const canvas = document.createElement('canvas')
  canvasContainer.value.appendChild(canvas)

  // 初始化 regl 并绑定到指定的 canvas
  const regl = reglLib({ canvas })
  const pointer = new Pointer(canvas)
  let morphAmount = 0

  // 设置 canvas 的宽高为 200px
  canvas.width = 200
  canvas.height = 200

  pointer.addPressingListener((e) => {
    morphAmount += e.detail * 0.1
  })

  const draw = regl({
    frag: `
        precision mediump float;
        uniform vec2 uResolution;
        uniform float uTime;
        uniform vec2 uMouse;
        uniform float uMorph;
        uniform vec3 uColor; // 基础颜色
        void main() {
        vec2 p = (2.0 * gl_FragCoord.xy - uResolution) / min(uResolution.x, uResolution.y);
        float t = uTime * 0.07 + uMorph;
        // 创建动态彩色效果，使用基础颜色作为起点
        vec3 color = uColor;
        
        color.r = uColor.r * (0.5 + 0.5 * sin(p.x + t));
        color.g = uColor.g * (0.5 + 0.5 * sin(p.y + t * 1.5));
        color.b = uColor.b * (0.5 + 0.5 * sin(length(p) + t * 0.8));
        gl_FragColor = vec4(color, 1.0);
        }
      `,
    vert: `
        attribute vec2 position;
        void main() {
        gl_Position = vec4(position, 0, 1);
        }
      `,
    attributes: {
      position: regl.buffer([
        [-1, -1],
        [1, -1],
        [-1, 1],
        [-1, 1],
        [1, 1],
        [1, -1]
      ])
    },
    uniforms: {
      uResolution: ({ viewportWidth, viewportHeight }) => [viewportWidth, viewportHeight],
      uTime: ({ tick }) => 0.1 * tick * props.speed, // 动态调整速度
      uMouse: () => [pointer.position.x, pointer.position.y],
      uMorph: () => morphAmount,
      uColor: () => props.color // 添加颜色参数
    },
    count: 6
  })

  // 动态调整 canvas 大小
  const resizeCanvas = () => {
    canvas.width = canvasContainer.value.offsetWidth
    canvas.height = canvasContainer.value.offsetHeight
  }

  resizeCanvas() // 初始化时调整大小
  window.addEventListener('resize', resizeCanvas) // 监听窗口大小变化

  regl.frame(() => {
    draw()
  })
})

class Pointer {
  constructor(domElement) {
    this.dom = domElement
    this.position = new Vector2()
    this.pressure = 0.0
    this.isPressing = false
    this.addListeners()
  }

  addListeners() {
    this.dom.addEventListener('mousemove', this.onMove.bind(this), false)
    this.dom.addEventListener('mousedown', this.onDown.bind(this), false)
    this.dom.addEventListener('mouseup', this.onUp.bind(this), false)
  }

  onMove(e) {
    const rect = this.dom.getBoundingClientRect()
    this.position.set((e.clientX - rect.left) / rect.width, (e.clientY - rect.top) / rect.height)
  }

  onDown() {
    this.isPressing = true
  }

  onUp() {
    this.isPressing = false
  }

  addPressingListener(callback) {
    this.dom.addEventListener('Pointer.pressing', callback, false)
  }
}
onMounted(()=> {
    console.log(props.color);
    
})
</script>

<style scoped>
.canvas-container {
  width: 200px;
  height: 200px;
  position: relative;
  overflow: hidden;
  background-color: black;

}

.canvas-container canvas {
  width: 100%;
  height: 100%;
  display: block;
}

</style>
