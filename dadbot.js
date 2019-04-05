const Discord = require('discord.js');
const client = new Discord.Client();
const token = process.env.token;

client.on('ready', () => {console.log('Dad bot reporting for duty');});

var dadPattern = /^(?:i'm|im|i am) ?a? ([^\.\,\n]*)/i

client.on('message', message => {
    if (message.author.bot) return;

    var messageContent = message.content;
    var react = messageContent.match(dadPattern);

    console.log("Got message: "+messageContent);
    console.log("Got reaction: "+react);

    if (react) {
        message.channel.send("Hi "+react[1]+", I'm Dadbot!");
        console.log("Said hi to: "+react[1]);
    }
});

client.login(token);
