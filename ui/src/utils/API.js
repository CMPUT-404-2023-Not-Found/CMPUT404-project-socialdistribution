/*
2023-02-26
utils/API.js
*/
// Constants

class API {
    API_URL=process.env.REACT_APP_API_URL;
    async get(path, token) {
        const url = this.API_URL + path;
        const response = await fetch(url, {
            headers: {
                'Authorization': 'Bearer ' + String(token)
            }
        });
        const data = await response.json();
        return [ response, (data ? data : false)]
    }
}

export default new API();
