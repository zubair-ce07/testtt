import BaseService from '../../base.service';

class UserService extends BaseService {
  ACTION = './users';

  register(user) {
    const action = './register';
    const url = new URL(action, BaseService.BASE_URL);
    return this.fetch(url, 'POST', user);
  }

  async login(credentials) {
    const action = './login';
    const url = new URL(action, BaseService.BASE_URL);
    return this.fetch(url, 'POST', credentials);
  }
}

export default UserService;
