import BaseService from '../../base.service';

class BlogsService extends BaseService {
  ACTION = './blogs/';

  get(params) {
    return super.get(params, false);
  }

  getById(id) {
    return super.getById(id, false);
  }

  getTags(params) {
    const url = new URL('./blogs/tags/', BaseService.BASE_URL);
    url.search = new URLSearchParams(params);
    return this.fetch(url, 'GET', null, false);
  }
}

export default BlogsService;
