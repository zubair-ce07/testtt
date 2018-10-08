import BaseService from '../../base.service';

class CommentsService extends BaseService {
  ACTION = './blogs/comments/';

  get(params) {
    return super.get(params, false);
  }

  getById(id) {
    return super.getById(id, false);
  }
}

export default CommentsService;
