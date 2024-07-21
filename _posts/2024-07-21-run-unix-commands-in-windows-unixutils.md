---
layout: post
title: Run Unix commands in Windows CMD using UnxUtils
categories: [blog]
tags: [cmd, commandline, unix, unxutils]
---

With the recent [blue screen of death incident](https://www.nytimes.com/live/2024/07/19/business/global-tech-outage/crowdstrike-outage-flights-banks), I kind of thought about how much I missed working in Linux. 

I've also been mentally resisting to learn more CMD commands for a while now. That said, using UnxUtils is a way to use Unix commands in Windows *without the need to activate or install Windows Subsystem for Linux (WSL)*.

Here's how to setup UnxUtils:

1. Download the [zip file](https://sourceforge.net/projects/unxutils).
2. Unzip the file to a desired location in the local machine.
3. Add the path of the executables (e.g. `D:\Programs\UnxUtils\usr\local\wbin`) to Windows environment variables. See [these steps](https://helpdeskgeek.com/windows-10/add-windows-path-environment-variable/), or below:
    - Search for "Envrionment variables" using Windows taskbar
    - Select "Edit environment variables for your account"
    - Add the path to the executable files in either User `PATH` variable (to make the execs available to current user only) or System `PATH` variable (to make them available to other users).
4. Refresh terminals. If existing terminals are open, close and open another instance to refresh. To refresh VS Code terminal, close VS Code, open a new CMD terminal, type `code`. This will open a new instance of VS Code with environment variables refreshed. 
5. Check to see if the commands are available. Open a new terminal and type `ls`, `cat`, or test creating a new file using `touch` e.g. `touch text.file`.

If these commands ran without issues, Unix commands are now available in Windows CMD.

This isn't the point of this post but the BSOD incident also makes me think how global tech infrastructure is concernedly fragile - despite all the discussions around cloud computing (replication zones), blockchain and AGI for years. There's only a handful of tech companies that dominate the industry which, unfortunately in this case, includes infrastructures in critical services such as healthcare. Tech has had its fair number of issues such as layoffs, and tools in the internet somehow still manage to blame DEI. Yet incidents like this goes to show that there's so much invisible work to make modern digital infrastructure sound.


![Xkcd Dependency](https://imgs.xkcd.com/comics/dependency.png){" .normal}
_Reference: [xkcd](https://xkcd.com/2347/)_

#### References
- [UnxUtils](https://unxutils.sourceforge.net/)
- [Use unix commands in Windows](https://www.techlila.com/use-unix-commands-windows/)
- [VS Code Refresh Integrated Terminal](https://stackoverflow.com/questions/54653343/vs-code-refresh-integrated-terminal-environment-variables-without-restart-logout?rq=1)