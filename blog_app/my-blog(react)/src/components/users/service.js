import BaseService from '../../base-service';

class UsersService extends BaseService {
  ACTION = './user';

  register(user) {
    const action = './register';
    const url = new URL(action, BaseService.BASE_URL);
    return this.fetch(url, 'POST', user, false);
  }

  async signIn(credentials) {
    const action = './login';
    const url = new URL(action, BaseService.BASE_URL);
    const response = await this.fetch(url, 'POST', credentials, false);

    if (response.success) {
      localStorage.setItem('auth-token', response.data.token);
      response.data = response.data.user;
    }
    return response;
  }

  async signOut() {
    localStorage.clear();
    return { success: true };
  }

  update(object, authRequired) {
    return super.update('', object, authRequired);
  }

  getSignedInUser() {
    return super.get();
  }
}

export default UsersService;
