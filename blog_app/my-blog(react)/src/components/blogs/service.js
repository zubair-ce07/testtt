import BaseService from '../../base-service';

class BlogsService extends BaseService {
  ACTION = './blogs/';

  get(params) {
    return super.get(params, false);
  }

  getById(id) {
    return super.getById(id, false);
  }
}

export default BlogsService;
