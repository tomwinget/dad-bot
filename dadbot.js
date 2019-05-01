const Discord = require('discord.js');
const exec = require('child_process').execSync;
const client = new Discord.Client();
const token = process.env.token;

client.on('ready', () => {console.log('Dad bot reporting for duty');});

var dadPattern = /^(?:i’m|i'm|im|i am) ?a? ([^\.\,\n]*)/i

client.on('message', message => {
    if (message.author.bot) return;

    if(message.isMentioned(client.user)){
        var output = exec('curl -H \'Accept: text/plain\' -H \'User-Agent: dad-bot (github.com/tomwinget/dad-bot)\' https://icanhazdadjoke.com/', {encoding: 'utf-8'});
        console.log('Got joke: '+output);
        message.channel.send(output);
    }

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
