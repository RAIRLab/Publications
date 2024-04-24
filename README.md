
## RAIR Lab Publications

This publication repository, originally maintained by Michael Giancola on the RAIR Lab SVN (now maintained on the github),
functions as a complete list of publications produced by RAIR lab members during their time in the lab. Using github
actions, this repository will automatically scan DBLP for any publications that meet the inclusion criteria on the first of each month, and generate a pdf. This PDF will then be used on the main [RAIR Lab publications page](https://rair.cogsci.rpi.edu/publications/) (via an iframe to the pdf on github pages).  

## Updating
The file `members.json` contains a list of all current and past members. Each member has the following felids:
```
name: string of the members name, does not actually get used by the application.
id: A string with the DBLP pid of the person.
perm: a flag indicating if this person is a permanent member (IE. Selmer and Naveen)
```

## Inclusion Criterion

To be automatically classified as a lab paper, the paper must: 
1) Appear in the [DBLP](https://dblp.dagstuhl.de/) database.
2) Have at least two members appearing in the `members.json` list.
3) Have both members marked as a current members, to be considered a current member they must either
  1) Be marked as a permanent member in `members.json` with `"perm": true`. 
  2) Have this be their first RAIR Lab publication. 
  3) Have less than 8 years between their first RAIR Lab publication and now.

This system prevents situations such as a 2024 paper that both Selmer and Paul Bello are on, but no other lab members are 
from being considered a RAIR Lab publication. 