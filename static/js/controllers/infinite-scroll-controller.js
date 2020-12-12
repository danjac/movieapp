import { Controller } from 'stimulus';

import InfiniteScroll from 'infinite-scroll';

export default class extends Controller {
  static classes = ['append', 'status'];

  static values = {
    paginationUrl: String,
  };

  connect() {
    this.scroll = new InfiniteScroll(this.element, {
      append: '.' + this.appendClass,
      status: '.' + this.statusClass,
      path: this.paginationUrlValue,
      history: false,
    });
  }

  disconnect() {
    this.scroll = null;
  }
}
