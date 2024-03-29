/*
2023-02-26
utils/Backend.js
*/
// Constants

class Backend {
    API_URL=process.env.REACT_APP_API_URL;
    async get(path, token) {
        const url = this.API_URL + path;
        let response = null;
        try {
            response = await fetch(url, {
                headers: {
                    'Authorization': 'Bearer ' + String(token)
                }
            });
        } catch (error) {
            console.error('Failed to call backend. e ');
            console.error(error);
        }
        const data = response ? await response.json() : null;
        return [ response, (data ? data : false)]
    }

    async getDirect(path, token) {
        const url = path;
        let response = null;
        try {
            response = await fetch(url, {
                headers: {
                    'Authorization': 'Bearer ' + String(token)
                }
            });
        } catch (error) {
            console.error('Failed to call backend. e ');
            console.error(error);
        }
        const data = response ? await response.json() : null;
        return [ response, (data ? data : false)]
    }

    async post(path, token, requestData, requestDataType='application/json') {
        const url = this.API_URL + path;
        let response = null;
        try {
            response = await fetch(url, {
                headers: {
                    'Authorization': 'Bearer ' + String(token),
                    'Content-Type': requestDataType
                },
                method: 'post',
                body: requestData
            });
        } catch (error) {
            console.error('Failed to call backend. e ');
            console.error(error);
        }
        const responseData = response ? await response.json() : null;
        return [ response, (responseData ? responseData : false)]
    }

    async put(path, token, requestData, requestDataType='application/json') {
        const url = this.API_URL + path;
        let response = null;
        try {
            response = await fetch(url, {
                headers: {
                    'Authorization': 'Bearer ' + String(token),
                    'Content-Type': requestDataType ? requestDataType : null
                },
                method: 'put',
                body: requestData ? requestData : null
            });
        } catch (error) {
            console.error('Failed to call backend. e ');
            console.error(error);
        }
        const responseData = response ? await response.json() : null;
        return [ response, (responseData ? responseData : false)]
    }

    async delete(path, token) {
        const url = this.API_URL + path;
        const response = await fetch(url, {
            headers: {
                'Authorization': 'Bearer ' + String(token)
            },
            method: 'delete'
        });
        return response
    }
    
    async options(path, token) {
        const url = this.API_URL + path;
        let response = null;
        try {
            response = await fetch(url, {
                headers: {
                    'Authorization': 'Bearer ' + String(token)
                },
                method: 'options'
            });
        } catch (error) {
            console.error('Failed to call backend. e ');
            console.error(error);
        }
        const data = response ? await response.json() : null;
        return [ response, (data ? data : false)]
    }
}

export default new Backend();
