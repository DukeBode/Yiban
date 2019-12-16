const nunjucks = require('nunjucks')
const sha1 = require('sha1');

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
 * 消息模板
 */
let template = nunjucks.compile(
    '<xml>' +
    '<ToUserName><![CDATA[{{ toUserName }}]]></ToUserName>' +
    '<FromUserName><![CDATA[{{ fromUserName }}]]></FromUserName>' +
    '<CreateTime>{{ createTime }}</CreateTime>' +
    '<MsgType><![CDATA[{{ msgType }}]]></MsgType>' +
    '{% if msgType === "text" %}' +
    '<Content><![CDATA[{{ message.content }}]]></Content>' +
    '{% elif msgType === "image" %}' +
    '<Image>' +
    '<MediaUrl><![CDATA[{{ message.mediaurl }}]]></MediaUrl>' +
    '</Image>' +
    '{% elif msgType === "voice" %}' +
    '<Voice>' +
    '<item>' +
    '<MediaUrl><![CDATA[{{ message.mediaurl }}]]></MediaUrl>' +
    '<Length><![CDATA[ 10]]></Length>' +
    '</item>' +
    '</Voice>' +
    '{% elif msgType === "location" %}' +
    '<Address><![CDATA[{{ message.address }}]]></Address>' +
    '<Coordinates><![CDATA[{{ message.coordinates }}]]></Coordinates>' +
    '{% elif msgType === "link" %}' +
    '<Content><![CDATA[{{ message.url }}]]></Content>' +
    '{% elif msgType === "new" %}' +
    '<ArticleCount>{{ message.count }}</ArticleCount>' +
    '<Articles>' +
    '{% for article in message.articles %}' +
    '<item>' +
    '<Title><![CDATA[{{ article.title }}]]></Title> ' +
    '<Description><![CDATA[{{ article.description }}]]></Description>' +
    '<PicUrl><![CDATA[{{ article.picurl }}]]></PicUrl>' +
    '<Url><![CDATA[{{ article.url }}]]></Url>' +
    '</item>' +
    '{% endfor %}' +
    '</Articles>' +
    '{% endif %}' +
    '</xml>'
    )

/**
 * 内容回复模板封装
 * @param {String} msgType 
 * @param {*} fromUserName 
 * @param {*} toUserName 
 * @param {Object} message 
 */
let reply = (msgType, fromUserName, toUserName, message) => {
    return template.render({
        'toUserName': toUserName,
        'fromUserName': fromUserName,
        'createTime': Math.floor(new Date().getTime()/1000),
        'msgType': msgType,
        'message':message
    })
};

let middleware={}

middleware.checkSignature=checkSignature;
middleware.reply=reply;

module.exports = middleware;
