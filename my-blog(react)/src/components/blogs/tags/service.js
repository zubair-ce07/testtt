import BaseService from '../../../base-service';

class TagsService extends BaseService {
  ACTION = './blogs/tags/';

  get(params) {
    return super.get(params, false);
  }

  getById(id) {
    return super.getById(id, false);
  }
}

export default TagsService;
