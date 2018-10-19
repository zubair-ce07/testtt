import { NotificationManager } from 'react-notifications';

class BaseService {
  static BASE_URL = `${process.env.REACT_APP_API_URL}api/`;
  ACTION = './unknown';

  constructor() {
    if (new.target === BaseService) {
      throw new TypeError('Cannot construct Abstract instances directly');
    }
  }

  async fetch(url, method, data, authRequired = true) {
    const response = { success: false, code: null, data: {} };
    const headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    };

    if (authRequired) {
      const authToken = localStorage.getItem('auth-token');

      if (!authToken) {
        response.code = 401;
        NotificationManager.error('You are not signed in');
        response.message = 'You are not signed in';
        return response;
      }
      headers.Authorization = `Token ${authToken}`;
    }

    const options = {
      method: method || 'GET',
      mode: 'cors',
      headers
    };

    if (
      data &&
      options.method !== 'GET' &&
      options.method !== 'HEAD' &&
      options.method !== 'DELETE'
    ) {
      options.body = JSON.stringify(data);
    }

    try {
      const rawResponse = await fetch(url, options);

      if (rawResponse.ok) {
        response.success = true;
      }

      if (authRequired && rawResponse.status === 401) {
        localStorage.clear();
      }

      response.code = rawResponse.status;
      try {
        response.data = await rawResponse.json();
      } catch (error) {
        console.log('response is not valid json');
      }
    } catch (error) {
      NotificationManager.error('A network error occurred!');
      response.message = 'A network error occurred!';
    }

    return response;
  }

  get(params, authRequired) {
    const url = new URL(this.ACTION, BaseService.BASE_URL);
    url.search = new URLSearchParams(params);
    return this.fetch(url, 'GET', null, authRequired);
  }

  getById(id, authRequired) {
    const url = new URL(`${this.ACTION}${id}`, BaseService.BASE_URL);
    return this.fetch(url, 'GET', null, authRequired);
  }

  add(object, authRequired) {
    const url = new URL(this.ACTION, BaseService.BASE_URL);
    return this.fetch(url, 'POST', object, authRequired);
  }

  update(id, object, authRequired) {
    const url = new URL(`${this.ACTION}${id}`, BaseService.BASE_URL);
    return this.fetch(url, 'PATCH', object, authRequired);
  }

  delete(id, authRequired) {
    const url = new URL(`${this.ACTION}${id}`, BaseService.BASE_URL);
    return this.fetch(url, 'DELETE', null, authRequired);
  }
}

export default BaseService;
