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

    async post(path, token, requestData, requestDataType='application/json') {
        const url = this.API_URL + path;
        const response = await fetch(url, {
            headers: {
                'Authorization': 'Bearer ' + String(token),
                'Content-Type': requestDataType
            },
            method: 'post',
            body: requestData
        });
        const responseData = await response.json();
        return [ response, (responseData ? responseData : false)]
    }
}

export default new Backend();
