class BaseService {
  static BASE_URL = 'http://localhost:8000/api/';
  ACTION = './unknown';

  constructor() {
    if (new.target === BaseService) {
      throw new TypeError('Cannot construct Abstract instances directly');
    }
  }

  async fetch(url, method, data) {
    let response = { success: false, code: null };
    try {
      const rawResponse = await fetch(url, {
        method: method || 'GET',
        body: JSON.stringify(data),
        mode: 'cors',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        }
      });

      if (rawResponse.ok) {
        response.success = true;
      }

      response.code = rawResponse.status;
      response.data = await rawResponse.json();
    } catch (error) {
      response.message = 'A network error occured!';
    }

    return response;
  }

  get(params) {
    const url = new URL(this.ACTION, BaseService.BASE_URL);
    url.search = new URLSearchParams(params);
    return this.fetch(url);
  }

  getById(id) {
    const url = new URL(`${this.ACTION}/${id}`, BaseService.BASE_URL);
    return this.fetch(url);
  }

  add(object) {
    const url = new URL(this.ACTION, BaseService.BASE_URL);
    return this.fetch(url, 'POST', object);
  }

  update(id, object) {
    const url = new URL(`${this.ACTION}/${id}`, BaseService.BASE_URL);
    return this.fetch(url, 'PATCH', object);
  }

  delete(id) {
    const url = new URL(`${this.ACTION}/${id}`, BaseService.BASE_URL);
    return this.fetch(url, 'DELETE');
  }
}

export default BaseService;
