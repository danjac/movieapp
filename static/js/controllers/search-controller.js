import axios from 'axios';
import debounce from 'lodash.debounce';
import throttle from 'lodash.throttle';
import { Controller } from 'stimulus';

export default class extends Controller {
  static targets = ['input', 'results', 'loading', 'result'];
  static values = { url: String, showResults: Boolean, search: String };

  initialize() {
    this.search = debounce(this.search, 500).bind(this);
    this.search = throttle(this.search, 500).bind(this);
  }

  connect() {
    this.resultIndex = 0;
  }

  search(event) {
    this.searchValue = this.inputTarget.value.trim();
  }

  close() {
    this.showResultsValue = false;
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
        this.move(event);
        break;
      default:
    }
  }

  move(event) {
    if (!this.showResultsValue || this.resultTargets.length === 0) {
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

  showResultsValueChanged() {
    if (!this.showResultsValue) {
      this.resultsTarget.innerHTML = '';
      this.resultsTarget.classList.add('hidden');
      this.resultIndex = 0;
    } else {
      this.resultsTarget.classList.remove('hidden');
    }
  }

  async searchValueChanged() {
    if (this.searchValue.length > 2) {
      this.resultsTarget.classList.add('hidden');
      this.loadingTarget.classList.remove('hidden');
      try {
        const response = await axios.get(this.urlValue, {
          params: {
            search: this.searchValue,
          },
        });
        this.resultsTarget.innerHTML = response.data;
        this.resultsTarget.classList.remove('hidden');
        this.showResultsValue = true;
      } finally {
        this.loadingTarget.classList.add('hidden');
      }
    } else {
      this.close();
    }
  }
}
