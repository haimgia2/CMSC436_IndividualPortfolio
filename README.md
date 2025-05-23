# CMSC436_IndividualPortfolio

# Item 1: Shifting Incomes for American Jobs - Chapter 5 Activity
Source:

https://flowingdata.com/2016/06/28/distributions-of-annual-income/

This curation is one of my favorite vis's during the Chapter 5 Activity. I like how they were able to implement animation with the moving bubble as well as interaction with the buttons of each decade to show the change in distribution of incomes for the different markets. At the same time, I like how simplistic it looked. The curator wasn't trying to overload the viewer with too much information, and I was able to understand what the vis is about just by looking at it. The colors were distinct enough to see the differences between each row, and the text was easy to read as well. Overall, I found looking at this vis to be reflective.

During the Chapter 5 Activity, I felt that this vis did a good job in encoding different attributes. There were many attributes that were encoded, such as categorical attributes like job market and decades and quantitative attributes like income. They used points as their marks, and at first, I thought that the points represented the people in each occupation, but then I realized there would've been a lot more people in certain job markets and that too many points would make it hard to read. Now I deduced that each job market was probably normalized and that the points represent the distribution of people in each job market, making it a lot easier to understand. The vertical position represented the thresholds of each income, making each row look like its own dot clustered dot plot. And while other channels like horizontal position and color hue were redundantly encoding occupation, I still didn't mind it because it made it more easier to understand.

Moving forward, rather than encoding quantitative attributes with lines and bars like other generic vises, I should try to transform the data and encode other things like distribution and rate of change. I feel like by doing so, we can introduce a diferent side to the data, just like what this example did.

On a side note, looking at the vis made me realize not only how unevenly distributed each job market is to each other, but also how some people lie on the higher spectrum of income compared to others in the same job market.

# Item 3: Minecraft Interactive Network
As someone who used to play Minecraft all the time—and still hops back in from time to time—I’ve always been fascinated by the crafting mechanic, which I believe is what made Minecraft such a unique game. However, I often found it a hassle to search online for crafting recipes for specific items or to figure out what certain raw materials were used for.

Outside of class, I’m working on a sustained research project at the UMBC Data Management & Semantics (DAMS) Research Group called the IoT Knowledge Graph Project, where I work extensively with networks and graph databases. Since I already had experience with network visualization, I came up with the idea to display the relationships between Minecraft items as an interactive graph. This would allow all crafting recipes to be stored in a centralized, user-friendly database, avoiding the overwhelm of scrolling through chunks of text. In this network, nodes represent Minecraft items, and directed edges indicate that one item is used as an ingredient in crafting another. Clicking on an item also opens a sidebar that shows its crafting recipe.

Initially, I planned to scrape data from the official Minecraft wiki, but I found that the pages were too disorganized for reliable extraction. I pivoted to unofficial Minecraft websites, which had more structured representations of crafting recipes. However, I ran into issues with bot detection while scraping, which taught me the value of seeking out open-source datasets before resorting to scraping.

In the IoT Knowledge Graph project, we used ArangoDB to host the graph. Wanting to make my Minecraft network easy to host locally and customizable with interactive features like a sidebar, I built the visualization using Cytoscape and Dash. Cytoscape is known for its ability to render large graphs and its interactive capabilities. The network was hosted locally using Dash, and while learning Cytoscape was a challenge at first, I eventually got the hang of it. I also encountered performance issues due to the number of nodes, so I implemented caching of the original network to reduce load times after the initial render.

Throughout the process, I learned that different graph tools are suited for different use cases. Dash and Cytoscape are great for building clean, interactive networks, while heavier graph databases like ArangoDB or Neo4j are more appropriate for rendering networks with thousands of nodes and edges. I also attempted to cluster nodes by item type, but doing so caused overlapping among nodes and edges, which made the network harder to interpret. I'm still wondering if there’s an effective way to cluster nodes by item type without causing overlaps, and if so, whether it would make the Minecraft network easier to understand.

# Item 4: Sports Facilities Chloropleth Map across New York City

Sources:

https://data.cityofnewyork.us/d/qnem-b8re

https://docs.google.com/spreadsheets/d/1iIhwuLBlIus2n1EQ2a329jX4oJciXt9dEaxOFPpHfE8/edit?usp=sharing

https://www.nycgovparks.org/permits/

One of my project pitches was to build an interactive map of sports facilities. Initially, the idea started as a way to locate nearby tennis courts, since tennis is one of the main sports I play, but I decided to broaden the scope to general sports facilities to attract a wider audience of athletes. It also helped that general sports facility data was relatively easy to access through Data World. I used the open-source Athletic Facilities dataset provided by NYC’s Department of Parks and Recreation (DPR), which includes multipolygons of sports facilities, their zip codes, dimensions, surface types, and the primary sport played at each location. The dataset also came with a data dictionary, which made it easy to interpret and work with. It was detailed and comprehensive enough to support a meaningful data visualization.

While building this project, I realized that creating choropleth maps can be quite challenging. Mapping the sports facilities required the use of multipolygons, so I had to learn how to visualize these using GeoPandas. I also ran into rendering issues. Even though the dataset only covers facilities in NYC, it includes about 6,000 entries, which made rendering slow and difficult to test. I began by working with a smaller subset of the data before gradually expanding to the full dataset. To improve performance, I implemented caching for the rendered maps, especially when applying different filters, so the map wouldn’t have to be fully redrawn each time.

The choropleth map was built using PyDeck and Dash, which allowed me to add interactive features like filtering by sport, zip code, and surface type, and ideally clicking on a facility to show more details in a sidebar. However, due to the complexity of the implementation and time constraints, I was only able to support filtering by primary sport, along with zoom and hover features.

If I work with large-scale maps or geovisualizations again, such as those used in graph databases, I now understand the importance of caching to improve rendering speed and usability.

This was my first time working with geovisualizations, so I'm still getting used to the process. If I get the chance to improve this project, I’d like to implement the interactive features I wasn’t able to complete, such as displaying additional facility details on click. I also want to include more attributes beyond just the primary sport and unique ID, and further optimize the rendering performance, as the map still takes time to load.
