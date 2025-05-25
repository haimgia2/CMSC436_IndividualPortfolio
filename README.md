# CMSC436_IndividualPortfolio

# Item 1: Shifting Incomes for American Jobs - Chapter 5 Activity
## Source

https://flowingdata.com/2016/06/28/distributions-of-annual-income/

This curation was one of my favorite visualizations from the Chapter 5 Activity. I appreciated how it combined animation—through the moving bubbles—with interactive buttons that allowed viewers to explore changes in income distribution across different markets over several decades. At the same time, I admired its simplicity. The curator avoided overloading the viewer with too much information, and I was able to understand the purpose of the visualization at a glance. The colors were distinct enough to clearly differentiate between rows, and the text was clean and easy to read. Overall, I found this visualization to be both engaging and reflective.

During the activity, I felt that this visualization did a great job encoding multiple attributes. It included categorical attributes like job market and decade, as well as quantitative attributes like income. The use of points as marks was especially effective. Initially, I thought each point represented an individual person in a given occupation, but then I realized that would have led to an overwhelming number of points, especially in more populated job markets. I later deduced that the data was likely normalized, with the points representing the distribution of people within each job market—an approach that made the visualization easier to interpret. The vertical position encoded income thresholds, turning each row into a clustered dot plot. While channels like horizontal position and color hue were redundantly used to encode occupation, I actually found this redundancy helpful in reinforcing understanding.

Looking ahead, rather than relying solely on traditional bar or line charts to represent quantitative data, I want to explore alternative encodings like distribution or rate of change. This approach, as shown in this example, can reveal different dimensions of the data and make the visualization more insightful.

On a side note, this visualization also made me reflect on how unevenly distributed incomes are across different job markets—and how, even within the same market, individuals can lie at vastly different points on the income spectrum.

# Item 2: Visualizing the School of Design in the Polytechnic University of Milan - Best/Worst Vis Bake-Off
## Source

https://densitydesign.org/2013/04/visualizing-the-school-of-design/

This curation was the one I selected for the Best Vis Bake-Off. It was created by DensityDesign, a design research lab at the Polytechnic University of Milan in Italy. The purpose of the visualization was to depict the career and higher education paths taken by students from the university’s School of Design. I really appreciated how the designers were able to condense a large amount of complex information into a single, visually appealing, and easy-to-understand artifact.

One key takeaway from this visualization is that you don’t necessarily need animation or interactivity to make a visualization impactful. The designers used a thoughtful combination of visual idioms—including Sankey diagrams to show the distribution of students across various paths, donut charts and stacked bar charts to represent ratios of students (e.g., college level, credits, areas of study), and histograms to display the frequency of graduating scores. I also appreciated their effective use of visual channels, especially horizontal and vertical position. As you follow the Sankey graph from left to right, it illustrates the progression of students through higher levels of education (Bachelor’s, Master’s, and PhD). The vertical position seems to indicate students who choose to enter the workforce at different levels of education. The Sankey diagram resembled a large, flowing filter, which made the data engaging to analyze.

Their color scheme was another strength—distinct yet subtle, visually pleasing without being distracting. It was clear that the creators put careful thought into their choice of idioms, visual channels, and color palette, all while opting out of animation and interactivity. While interactivity and animation can certainly enhance a visualization, I found this static visualization just as compelling—it invited viewers to explore and interpret the data at their own pace.

Outside of class, I’d like to experiment with new idioms like Sankey diagrams and donut charts. I’m still most familiar with traditional bar and line charts, so I want to continue exploring how other idioms can be even more effective, especially when combined. Inspired by this visualization, I’m interested in trying to integrate multiple idioms in a single view to see how they can complement one another and reveal deeper insights than they could individually.

On a side note, as someone in STEM, I’m not very familiar with the career trajectories of design-focused majors. Thanks to this visualization, I gained a better understanding of how many design students pursue advanced degrees and the specific areas within the field they choose to enter.



# Item 3: Minecraft Interactive Network
## Source

https://www.minecraftcrafting.info/

## Directions
1. make a new python environment
   ```
   pip install virtualenv
   python -m venv minecraft_env
   ```
2. activate your python environment
3. install the required dependencies in the requirements.txt
   ```
   pip install -r minecraft/requirements.txt 
   ```
4. run the code
   ```
   python minecraft_final.py
   ```

As someone who used to play Minecraft all the time—and still hops back in from time to time—I’ve always been fascinated by the crafting mechanic, which I believe is what made Minecraft such a unique game. However, I often found it a hassle to search online for crafting recipes for specific items or to figure out what certain raw materials were used for.

Outside of class, I’m working on a sustained research project at the UMBC Data Management & Semantics (DAMS) Research Group called the IoT Knowledge Graph Project, where I work extensively with networks and graph databases. Since I already had experience with network visualization, I came up with the idea to display the relationships between Minecraft items as an interactive graph. This would allow all crafting recipes to be stored in a centralized, user-friendly database, avoiding the overwhelm of scrolling through chunks of text. In this network, nodes represent Minecraft items, and directed edges indicate that one item is used as an ingredient in crafting another. Clicking on an item also opens a sidebar that shows its crafting recipe.

Initially, I planned to scrape data from the official Minecraft wiki, but I found that the pages were too disorganized for reliable extraction. I pivoted to unofficial Minecraft websites, which had more structured representations of crafting recipes. However, I ran into issues with bot detection while scraping, which taught me the value of seeking out open-source datasets before resorting to scraping.

In the IoT Knowledge Graph project, we used ArangoDB to host the graph. Wanting to make my Minecraft network easy to host locally and customizable with interactive features like a sidebar, I built the visualization using Cytoscape and Dash. Cytoscape is known for its ability to render large graphs and its interactive capabilities. The network was hosted locally using Dash, and while learning Cytoscape was a challenge at first, I eventually got the hang of it. I also encountered performance issues due to the number of nodes, so I implemented caching of the original network to reduce load times after the initial render.

Throughout the process, I learned that different graph tools are suited for different use cases. Dash and Cytoscape are great for building clean, interactive networks, while heavier graph databases like ArangoDB or Neo4j are more appropriate for rendering networks with thousands of nodes and edges. I also attempted to cluster nodes by item type, but doing so caused overlapping among nodes and edges, which made the network harder to interpret. I'm still wondering if there’s an effective way to cluster nodes by item type without causing overlaps, and if so, whether it would make the Minecraft network easier to understand.

# Item 4: Sports Facilities Chloropleth Map across New York City
## Sources

https://data.cityofnewyork.us/d/qnem-b8re

https://docs.google.com/spreadsheets/d/1iIhwuLBlIus2n1EQ2a329jX4oJciXt9dEaxOFPpHfE8/edit?usp=sharing

https://www.nycgovparks.org/permits/

## Directions
1. make a new python environment
   ```
   pip install virtualenv
   python -m venv sports_env
   ```
2. activate your python environment
3. install the required dependencies in the requirements.txt
   ```
   pip install -r sports_facilities/requirements.txt 
   ``` 
4. run the code
   ```
   python sports_app.py
   ```

One of my project pitches was to build an interactive map of sports facilities. Initially, the idea started as a way to locate nearby tennis courts, since tennis is one of the main sports I play, but I decided to broaden the scope to general sports facilities to attract a wider audience of athletes. It also helped that general sports facility data was relatively easy to access through Data World. I used the open-source Athletic Facilities dataset provided by NYC’s Department of Parks and Recreation (DPR), which includes multipolygons of sports facilities, their zip codes, dimensions, surface types, and the primary sport played at each location. The dataset also came with a data dictionary, which made it easy to interpret and work with. It was detailed and comprehensive enough to support a meaningful data visualization.

While building this project, I realized that creating choropleth maps can be quite challenging. Mapping the sports facilities required the use of multipolygons, so I had to learn how to visualize these using GeoPandas. I also ran into rendering issues. Even though the dataset only covers facilities in NYC, it includes about 6,000 entries, which made rendering slow and difficult to test. I began by working with a smaller subset of the data before gradually expanding to the full dataset. To improve performance, I implemented caching for the rendered maps, especially when applying different filters, so the map wouldn’t have to be fully redrawn each time.

The choropleth map was built using PyDeck and Dash, which allowed me to add interactive features like filtering by sport, zip code, and surface type, and ideally clicking on a facility to show more details in a sidebar. However, due to the complexity of the implementation and time constraints, I was only able to support filtering by primary sport, along with zoom and hover features.

If I work with large-scale maps or geovisualizations again, such as those used in graph databases, I now understand the importance of caching to improve rendering speed and usability.

This was my first time working with geovisualizations, so I'm still getting used to the process. If I get the chance to improve this project, I’d like to implement the interactive features I wasn’t able to complete, such as displaying additional facility details on click. I also want to include more attributes beyond just the primary sport and unique ID, and further optimize the rendering performance, as the map still takes time to load.
