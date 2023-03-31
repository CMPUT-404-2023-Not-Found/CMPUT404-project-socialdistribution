/*
2023-03-14
ui/src/utils/Utils.js

*/

export function getHostFromURL(myString) {
    let ret = '';
    try {
        const url = new URL(myString)
        ret = url.protocol + '//' + url.hostname;
    } catch (e) {
        console.error('Invalid url for ' + myString);
    }
    return ret;
}

/**
 * 
 * @param {string} myString A valid URL that looks like 'http://somesite.com/api/authors/1234/posts/5678
 * @returns The ending UUID, for example 5678, from a URL or null
 */
export function getUUIDFromURL(myString) {
    let ret = null;
    try {
        const url = new URL(myString)
        const path = url.pathname;
        const path_array = path.split('/');
        let uuid = path_array[path_array.length - 1]
        return (uuid.endsWith('/')) ?  uuid.slice(0, -1) : uuid;
    } catch (e) {
        console.error('Invalid url for ' + myString);
        return ret;
    }
}

/**
 * 
 * @param {string} myString
 * @returns Append '/inbox/' to myString
 */
export function getInboxUrl(myString) {
    let inboxUrl;
    inboxUrl = myString.endsWith('/') ? myString + 'inbox/' : myString + '/inbox/';
    return inboxUrl;
}

/**
 * 
 * @param {Object} myObject 
 * @returns True if myObject is an empty Object
 */
export function isObjectEmpty(myObject) {
    return (Object.keys(myObject).length <= 0 && myObject.constructor === Object);
}

/*
This code is from a forum question and answer post from Pavlo on 2017-04-18, retrieved on 2023-03-25 from stackoverflow.com
forum question and answer here:
https://stackoverflow.com/questions/5717093/check-if-a-javascript-string-is-a-url
*/
/**
 * 
 * @param {string} myString 
 * @returns True if myString is a valid URL
 */
export function isValidHttpUrl(myString) {
    let url;
    try {
        url = new URL(myString);
    } catch(e) {
        console.error('Invalid url for ' + myString);
        return false;
    }
    return url.protocol === 'http:' || url.protocol === 'https:';
}

/**
 * 
 * @param {string} myURL 
 * @returns True if myURL host is localhost else False
 */
export function isURLLocalhost(myURL) {
    let url;
    try {
        url = new URL(myURL);
    } catch(e) {
        console.error('Invalid url for ' + myURL);
        return false;
    }
    return url.host.includes('localhost')
}

/**
 * 
 * @param {string} myURL A URL string
 * @returns The path & query params of myURL
 */
export function parsePathFromURL(myURL) {
    let url;
    try {
        url = new URL(myURL);
    } catch(e) {
        console.error('Failed to construct URL from string' + myURL);
        return '/';
    }
    return url.pathname;
}

/**
 * Convert a UTC datetime string to local time
 * @param utcDateString A UTC ISO-8601 datetime string.
 * @returns Date string for local time
 */
export function utcToLocal(utcDatetimeString) {
    return new Date(utcDatetimeString).toDateString();
}
