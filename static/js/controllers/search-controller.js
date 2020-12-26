import debounce from 'lodash.debounce';
import { Controller } from 'stimulus';

export default class extends Controller {
  static targets = ['input', 'results', 'result'];
  static values = { search: String };

  initialize() {
    this.search = debounce(this.search, 500).bind(this);
  }

  connect() {
    this.resultIndex = 0;
  }

  search(event) {
    this.searchValue = this.inputTarget.value.trim();
  }

  close() {
    this.resultsTarget.innerHTML = '';
  }

  keydown(event) {
    // window key events
    switch (event.keyCode) {
      case 27: // esc:
        this.close();
        break;
      case 191: // forward slash
        this.inputTarget.focus();
        break;
      case 40: // key down
      case 38: // key up
        this.navigateResults(event);
        break;
      default:
    }
  }

  navigateResults(event) {
    // focus up/down arrow navigation through results
    if (!this.resultTargets.length === 0) {
      return;
    }

    event.preventDefault();
    event.stopPropagation();

    const position = event.keyCode === 38 ? -1 : 1;

    const target = this.resultTargets[this.resultIndex];

    if (target) {
      target.focus();
      this.resultIndex += position;
    } else {
      this.inputTarget.focus();
      this.resultIndex = 0;
    }
  }

  async searchValueChanged() {
    if (this.searchValue.length > 2) {
      this.triggerSubmit();
    }
  }

  triggerSubmit() {
    if (this.element.requestSubmit) {
      this.element.requestSubmit();
    } else {
      // fallback for older browsers
      this.element.dispatchEvent(new CustomEvent('submit', { bubbles: true }));
    }
  }
}
