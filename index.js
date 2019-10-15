const Koa = require('koa');
const router = require('koa-router')();
const yiban = require("yiban-mp");
const xmlParser = require("koa-xml-body");
const app = new Koa();

let config = {
    token: "d3a8a8bd0e444d23db5ef5d3e10eb9b2",
    appid: ""
}

router
    .get('/', ctx => {
        console.log(ctx.query);
        ctx.body=yiban.checkSignature(ctx.query,config.token);
    })
.post('/',ctx=>{
        console.log(ctx.request.body);
        ctx.type = 'json';
        ctx.body = "";
//        ctx.body = yiban.reply("text",ctx.request.body.xml.ToUserName,ctx.request.body.xml.FromUserName,{"content":"hello"});
        console.log(ctx.body);
    })

app.use(xmlParser());
// 挂载路由实例
app.use(router.routes()).use(router.allowedMethods());

const port = 5151;

// 端口监听
app.listen(port);
console.log('Server running at http://127.0.0.1:' + port);
