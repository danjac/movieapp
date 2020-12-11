import { Controller } from 'stimulus';

export default class extends Controller {
  static targets = ['container'];

  open(event) {
    const { content } = event.detail;
    this.containerTarget.append(content);
    this.element.classList.remove('hidden');
  }

  close() {
    this.element.classList.add('hidden');
    this.containerTarget.innerHTML = '';
  }

  closeOnEsc(event) {
    console.log(event.keyCode);
    if (event.keyCode === 27) {
      this.close();
    }
  }
}
