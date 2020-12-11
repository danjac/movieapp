import { Controller } from 'stimulus';
import { useDispatch } from 'stimulus-use';

export default class extends Controller {
  static targets = ['content'];

  connect() {
    useDispatch(this);
  }

  open(event) {
    event.preventDefault();
    event.stopPropagation();
    const clone = this.contentTarget.content.cloneNode(true);
    this.dispatch('open', { content: clone });
  }
}
