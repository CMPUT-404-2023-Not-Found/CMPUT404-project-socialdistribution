/*
2023-02-26
utils/Backend.js
*/
// Constants

class Backend {
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

export default new Backend();
