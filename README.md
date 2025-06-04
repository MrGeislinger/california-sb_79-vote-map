# Interactive Map of State Senator Voting on SB 79 California Bill with Contact Info

View the map broken by district at https://blog.mrgeislinger.com/california-sb_79-vote-map

![Example map plot of CA districts colored in green, red, or gray. Title "California State Senators Vote on SB 79 Bill Make sure to thank (or complain) to your senator". Shows gray box from mouse hover of Senator Time Grayson with voting info, district number,  website, and contact phone number](images/example-map.png)

## Background 

The [SB-79 Housing development bill](https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202520260SB79) passed on 2025 June 3rd.

I'm no expert, but many have said this is a huge win for home development _and_
transit development by allowing more multi-family housing to be built near
transit stops (busses & trains). See https://cayimby.org/legislation/sb-79/

Excited Californians were talking about making sure to call up their senator
to thank them for voting yes. Although contact information is available on
https://www.senate.ca.gov/senators, I realized it wasn't easy for the typical
person to find their senator, find out how they voted on this bill, and then
how to contact them.

So that night I quickly threw together this interactive map. (Sorry the code & 
map are not perfect!) Feel free to take what's there for your own use!


## Running the Code

### Prerequisite

#### OPTIONAL: Create a Virtual Environment

It's typically best to work in a virtual environment which you can use
whatever you're comfortable with.

For example, using `venv` you might do something like this:

```bash
python3 -m venv env
source env/bin/activate
```

#### Install Required Libraries

There is a provided `requirements.txt` that are needed for pulling the data & 
creating the map. It can be installed like so:

```bash
pip install -r requirements.txt
```

### Pull Data

You should simply only need to run `pull-data.py`

```bash
python3 pull-data.py
```

This will use the voting information from https://www.senate.ca.gov/senators and 
the local `vote_data.csv` (manually created) that holds how the voting for SB-79 
went.

The script will then create a `senators_with_votes.csv` file (provided in this
repo for convenience).


### Creating the Map

You should simply only need to run `map.py`

```bash
python3 map.py
```

This will use the local file `senators_with_votes.csv` and pull the district 
boundaries from https://gis.data.ca.gov/datasets/CDEGIS::senate-districts/explore.

It will ultimately create the map in `index.html` which can be hosted as a
static page.
