---
layout: post
title: Pokemon Dashboard (First Generation)
categories:
- blog
---

Recently, I picked up my console and started playing Pokemon Fire Red again. At this point, I can't count how many times I've played and re-played that game. It's kind of nostalgic having been born in that era of video games. And of course, First Gen Pokemons are still close to my heart and used to be able to name all 100+ Pokemons. (Now, I've forgotten and I can't find the original series!)

<center><img src="https://overplay.com.br/wp-content/uploads/2022/06/pokemon-firered.jpg" alt="Pokemon Fire Red Version" width="200"/>
<small>Photo Credit: Overplay</small></center>

I thought it will be nice to do a project for myself and since I'm reviewing PowerBI, I thought to have the information served up in a dashboard.


I've extracted the data from the [Poke API](https://pokeapi.co/) using Python. For this, I'm mostly interested in the first 151 Pokemons, their abilities, types, and moves. I've also extracted data on their relationship with other types i.e. whether they're resistant or not. 

Here is the front page of the dasboard

<center><img src="/assets/images/pokemon-dashboard-front.png" alt="pokemon-dashboard-front" width="500"/></center>

There's a hidden filter pane toggled by the "Filter Stats" button that enables selection of Pokemons based on different statistics (Mewtwo and the legendary Pokemons have very low capture rates!)
<center><img src="/assets/images/pokemon-dashboard-front-filter.png" alt="pokemon-dashboard-front-filter" width="200"/></center>

There is also a drill-through page that shows more details about a Pokemon. I never knew that Pokemons could have many moves! For example, Charmander here can learn a total of 105.
<center><img src="/assets/images/pokemon-dashboard-drill-through.png" alt="pokemon-dashboard-drill-through" width="500"/></center>

I've also added a hover functionality to show the description of each move and ability. 

<center><img src="/assets/images/pokemon-dashboard-hover.png" alt="pokemon-dashboard-hover" width="500"/></center>


Here is how the model is set up.

<center><img src="/assets/images/pokemon-dashboard-model.png" alt="pokemon-dashboard-model" width="700"/></center>


I was careful to have the dashboard render well on the dimensions of an iPad so that I can try it on the mobile app. 

Here is how it's used: During a battle, open up your or your opponent's Pokemon description on the dashboard and strategize based on the moves, move types and stats.

<center><img src="/assets/images/pokemon-demo.jpg" alt="pokemon-demo" width="500"/></center>


Very self-serving indeed! 

Here is my favorite Pokemon, Togepi!

<center><img src="https://vignette3.wikia.nocookie.net/pokemon/images/f/f6/175Togepi_OS_anime_3.png/revision/latest?cb=20170628031231" alt="togepi" width="150"/>
<small>Photo Credit: Pokemon Wiki</small></center>


Which is sadly at #175 so I wasn't able to add the info in the dashbard. 😅

Anyway, I had fun doing this and will expand the script and update the dashboard when I get the chance. Could probably also try other games that I like and other interests - it's much more enjoyable to learn or review tech applications that way, at least for me.

The scripts repo is here [pokemon-dataset](https://github.com/maryletteroa/pokemon-dataset).

Here's the dashboard (Open in full screen)

<iframe title="pokemon" width="600" height="373.5" src="https://app.powerbi.com/view?r=eyJrIjoiZDAxOWUwYzMtY2QzZS00YzAyLWFmMmUtOTlhODNiNzg0ZDA4IiwidCI6Ijg4NWVhN2NiLWQ4YjUtNGQ2Ni1hNGRjLTQ0MDM5MzcwM2FjMCIsImMiOjEwfQ%3D%3D" frameborder="0" allowFullScreen="true"></iframe>

<small>
Log:<br>
-2024-04-20 Initial version of the dashboard as described in this post
</small>