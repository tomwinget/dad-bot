const Discord = require('discord.js');
const exec = require('child_process').execSync;
const client = new Discord.Client();
const token = process.env.dadToken;

client.on('ready', () => {console.log('Dad bot reporting for duty');});

var dadPattern = /^(?:i’m|i'm|im|i am) ?a? ([^\.\,\n]*)/i;
var alphaPattern = /^[^a-z]+$/i;

client.on('message', message => {
    if (message.author.bot) return;

    if(message.isMentioned(client.user)){
        var output = exec('curl -H \'Accept: text/plain\' -H \'User-Agent: dad-bot (github.com/tomwinget/dad-bot)\' https://icanhazdadjoke.com/', {encoding: 'utf-8'});
        console.log('Got joke: '+output);
        message.channel.send(output);
    }

    var messageContent = message.content;
    var react = messageContent.match(dadPattern);

    if (react) {
        message.channel.send("Hi "+react[1]+", I'm Dadbot!");
        console.log("Said hi to: "+react[1]);
        message.member.setNickname(react[1].substr(0,32))
            .then(console.log("Set nickname for "+message.member.displayName))
            .catch(console.error);
    }

    var alpha = messageContent.match(alphaPattern);
    if (!alpha && messageContent.length > 0 && messageContent === messageContent.toUpperCase()
        && messageContent != "LOL" && messageContent != "LMAO"){
        let user = message.author;
        var loudMessages = [`Now calm down ${user}!`, `No yelling in the house
            ${user}!`, `Lower your voice ${user}!`, `You're being too loud ${user}!`];
        var msg = loudMessages[Math.floor(Math.random() * loudMessages.length)];
        message.channel.send(msg);
        console.log("Told "+user+" to calm down");
    }
});

client.login(token);
