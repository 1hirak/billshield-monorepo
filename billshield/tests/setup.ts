import "@testing-library/jest-dom/vitest";

if (!globalThis.PointerEvent) {
  class PointerEvent extends MouseEvent {
    pointerId: number;
    pointerType: string;
    constructor(type: string, params: PointerEventInit = {}) {
      super(type, params);
      this.pointerId = params.pointerId ?? 0;
      this.pointerType = params.pointerType ?? "mouse";
    }
  }
  globalThis.PointerEvent = PointerEvent as typeof globalThis.PointerEvent;
}

if (!(Element.prototype as any).hasPointerCapture) {
  (Element.prototype as any).hasPointerCapture = () => false;
  (Element.prototype as any).setPointerCapture = () => {};
  (Element.prototype as any).releasePointerCapture = () => {};
}

if (!(Element.prototype as any).scrollIntoView) {
  (Element.prototype as any).scrollIntoView = () => {};
}

const originalGetComputedStyle = window.getComputedStyle;
window.getComputedStyle = (element, pseudoElt) => {
  const style = originalGetComputedStyle(element, pseudoElt);
  if (style.pointerEvents === "none") {
    return new Proxy(style, {
      get(target, prop) {
        if (prop === "pointerEvents") return "auto";
        return Reflect.get(target, prop);
      },
    });
  }
  return style;
};
