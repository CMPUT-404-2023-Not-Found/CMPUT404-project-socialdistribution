/*
2023-03-14
ui/src/utils/Utils.js

*/

/**
 * Convert a UTC datetime string to local time
 * @param utcDateString A UTC ISO-8601 datetime string.
 * @returns Date string for local time
 */
export function utcToLocal(utcDatetimeString) {
    return new Date(utcDatetimeString).toDateString();
}

/**
 * 
 * @param {Object} myObject 
 * @returns True if myObject is an empty Object
 */
export function isObjectEmpty(myObject) {
    return (Object.keys(myObject).length <= 0 && myObject.constructor === Object);
}
