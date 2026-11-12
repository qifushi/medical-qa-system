export class WaveView {
  private canvas!: HTMLCanvasElement;
  private ctx!: CanvasRenderingContext2D;
  private timer: number | null = null;
  private waveformTimer: ReturnType<typeof setInterval> | null = null;
  private _phase: number = 0;
  private settings: {
    elem: HTMLElement,     // DOM 元素
    width: number,        // 显示宽度
    height: number,       // 显示高度
    scale: number,        // 缩放系数（2）
    speed: number,        // 移动速度（9）
    phase: number,        // 相位（21.8）
    fps: number,          // 帧率（20）
    keep: boolean,        // 停止时保持波形
    lineWidth: number,    // 线条粗细（3）
    // 渐变色配置 [位置, 颜色, ...]
    linear1: [number, string, ...Array<number | string>];
    linear2: [number, string, ...Array<number | string>];
    linearBg: [number, string, ...Array<number | string>];
  };
  private pcmData: Float32Array | null = null;
  private pcmPos: number = 0;
  private sampleRate: number = 0;
  private inputTime: number = 0;
  private drawTime: number = 0;
  private isActive: boolean = false;

  private gradients: {
    linear1: CanvasGradient | null;
    linear2: CanvasGradient | null;
    linearBg: CanvasGradient | null;
  } = {
    linear1: null,
    linear2: null,
    linearBg: null
  };

  constructor(settings: any) {
    this.settings = {
      scale: 2,
      speed: 9,
      phase: 21.8,
      fps: 20,
      keep: true,
      lineWidth: 3,
      linear1: [0, "rgba(150,96,238,1)", 0.2, "rgba(170,79,249,1)", 1, "rgba(53,199,253,1)"],
      linear2: [0, "rgba(209,130,255,0.6)", 1, "rgba(53,199,255,0.6)"],
      linearBg: [0, "rgba(255,255,255,0.2)", 1, "rgba(54,197,252,0.2)"],
      ...settings
    };

    this.initCanvas();
  }

  private initCanvas() {
    const { width, height, scale, elem } = this.settings;
    
    this.canvas = document.createElement('canvas');
    this.canvas.width = width * scale;
    this.canvas.height = height * scale;
    this.canvas.style.width = '100%';
    this.canvas.style.height = '100%';
    
    this.ctx = this.canvas.getContext('2d')!;
    
    // 初始化渐变色
    this.gradients.linear1 = this.genLinear(this.ctx, width * scale, this.settings.linear1);
    this.gradients.linear2 = this.genLinear(this.ctx, width * scale, this.settings.linear2);
    this.gradients.linearBg = this.genLinear(this.ctx, height * scale, this.settings.linearBg, true);

    // 如果提供了 elem，直接将 canvas 添加到其中
    if (elem) {
      elem.innerHTML = '';
      elem.appendChild(this.canvas);
    }
  }

  private genLinear(ctx: CanvasRenderingContext2D, size: number, colors: [number, string, ...Array<number | string>], top?: boolean): CanvasGradient {
    const gradient = ctx.createLinearGradient(0, 0, top ? 0 : size, top ? size : 0);
    for (let i = 0; i < colors.length;) {
      const pos = colors[i++] as number;
      const color = colors[i++] as string;
      gradient.addColorStop(pos, color);
    }
    return gradient;
  }

  private genPath(frequency: number, amplitude: number, phase: number) {
    const { scale, width, height } = this.settings;
    const path = [];
    const maxAmplitude = height * scale / 2;

    for (let x = 0; x <= width * scale; x += scale) {
      const scaling = (1 + Math.cos(Math.PI + (x / (width * scale)) * 2 * Math.PI)) / 2;
      const y = scaling * maxAmplitude * amplitude * 
                Math.sin(2 * Math.PI * (x / (width * scale)) * frequency + phase) + maxAmplitude;
      path.push(y);
    }
    return path;
  }

  public input(pcmData: Float32Array, powerLevel: number, sampleRate: number) {
    this.sampleRate = sampleRate;
    this.pcmData = pcmData;
    this.pcmPos = 0;
    this.inputTime = Date.now();
    this.schedule();
  }

  private schedule() {
    const interval = Math.floor(1000 / this.settings.fps);
    if (!this.timer) {
      this.timer = window.setInterval(() => this.schedule(), interval);
    }

    const now = Date.now();
    if (now - this.drawTime < interval) {
      return;
    }
    this.drawTime = now;

    const bufferSize = this.sampleRate / this.settings.fps;
    const pcm = this.pcmData;
    if (!pcm) return;
    
    let pos = this.pcmPos;
    const len = Math.max(0, Math.min(bufferSize, pcm.length - pos));
    let sum = 0;
    
    for (let i = 0; i < len; i++, pos++) {
      sum += Math.abs(pcm[pos]);
    }
    this.pcmPos = pos;

    if (len || !this.settings.keep) {
      this.draw(this.calculatePowerLevel(sum, len));
    }
    
    if (!len && now - this.inputTime > 1300) {
      clearInterval(this.timer);
      this.timer = null;
    }
  }

  private calculatePowerLevel(sum: number, size: number) {
    if (size == 0) return 0;
    const power = Math.round(Math.min(100, Math.max(0, Math.sqrt(sum / size) * 100)));
    return power;
  }

  private draw(powerLevel: number) {
    const { scale, width, height, speed, fps, phase: phaseOffset } = this.settings;
    const ctx = this.ctx;

    const speedx = speed / fps;
    this._phase -= speedx;
    const phase2 = this._phase + speedx * phaseOffset;
    const amplitude = powerLevel / 100;

    const path1 = this.genPath(2, amplitude, this._phase);
    const path2 = this.genPath(1.8, amplitude, phase2);

    ctx.clearRect(0, 0, width * scale, height * scale);

    // 绘制背景
    this.drawBackground(path1, path2);
    
    // 绘制波形线
    this.drawPath(path2, this.gradients.linear2);
    this.drawPath(path1, this.gradients.linear1);
  }

  private drawBackground(path1: number[], path2: number[]) {
    const { scale, width } = this.settings;
    const ctx = this.ctx;

    ctx.beginPath();
    for (let i = 0, x = 0; x <= width * scale; i++, x += scale) {
      if (x == 0) {
        ctx.moveTo(x, path1[i]);
      } else {
        ctx.lineTo(x, path1[i]);
      }
    }
    
    for (let i = path1.length - 1, x = width * scale - scale; x >= 0; i--, x -= scale) {
      ctx.lineTo(x, path2[i]);
    }
    
    ctx.closePath();
    if (this.gradients.linearBg) {
      ctx.fillStyle = this.gradients.linearBg;
      ctx.fill();
    }
  }

  private drawPath(path: number[], gradient: CanvasGradient | null) {
    if (!gradient) return;
    
    const { scale, width, lineWidth } = this.settings;
    const ctx = this.ctx;

    ctx.beginPath();
    for (let i = 0, x = 0; x <= width * scale; i++, x += scale) {
      if (x == 0) {
        ctx.moveTo(x, path[i]);
      } else {
        ctx.lineTo(x, path[i]);
      }
    }
    
    ctx.lineWidth = lineWidth * scale;
    ctx.strokeStyle = gradient;
    ctx.stroke();
  }

  public getCanvas() {
    return this.canvas;
  }

  public destroy() {
    if (this.timer) {
      clearInterval(this.timer);
      this.timer = null;
    }
  }
} 