const nunjucks = require('nunjucks')
const sha1 = require('sha1');
nunjucks.configure('views', { autoescape: true });

/**
 * 检查签名
 * @param {Object} query GET params
 * @param {String} token Token
 */
let checkSignature = (query, token) => {
    let tmpArr = [token, query.timestamp, query.nonce];
    tmpArr.sort();
    return sha1(tmpArr.join("")) == query.signature?query.echostr:"";
};

/**
 * 内容回复模板封装
 * @param {String} msgType 
 * @param {*} fromUserName 
 * @param {*} toUserName 
 * @param {Object} message 
 */
let reply = (msgType, fromUserName, toUserName, message) => {
    return nunjucks.render('message.njk', {
        'toUserName': toUserName,
        'fromUserName': fromUserName,
        'createTime': new Date().getTime(),
        'msgType': msgType,
        'message':message
    })
};



module.exports = checkSignature;
