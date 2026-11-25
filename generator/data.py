# Facts for Florida State Tree & Landscaping LLC. Sources (captured 2026-11-25), see /workspace/ftree-research/notes.md:
#  FB = https://www.facebook.com/p/Florida-State-Tree-Landscaping-LLC-100083582852027/
#  GM = Google Business Profile (Tree service, 4874 SE 112 St Rd, Belleview FL 34420)
BASE = "https://rgwebd.github.io/floridastatetree-demo/"
NAME = "Florida State Tree & Landscaping"
LEGAL = "Florida State Tree & Landscaping LLC"
PHONE = "(352) 857-9472"; TEL = "+13528579472"          # GM + FB
PHONE2 = "(352) 454-9841"; TEL2 = "+13524549841"        # FB bio: "CALL OR TEXT US FOR A FREE ESTIMATE 352-857-9472 / 352-454-9841"
STREET = "4874 SE 112 St Rd"; CITY = "Belleview"; REGION = "FL"; ZIP = "34420"   # GM
GEO = (29.0453038, -82.0679205)                          # GM map pin
OWNER = "Harley Roth"                                    # FB post: "Call Harley Roth @ 352-857-9472 ..."
RATING = "5.0"; REVIEWS = 22                             # GM
TAGLINE = "Quality Work. Honest Service. Beautiful Results."   # logo on FB
FB = "https://www.facebook.com/p/Florida-State-Tree-Landscaping-LLC-100083582852027/"
MAPS = "https://www.google.com/maps/place/Florida+State+Tree+%26+Landscaping+LLC/@29.0453038,-82.0679205,17z/data=!4m6!3m5!1s0xfcb74f72141208b:0x3787b57b5eda292d"
AREAS = ["Marion County", "Sumter County", "Lady Lake", "The Villages"]   # FB details + featured flyer

REVIEWS_LIST = [
 dict(name="edward coleman", meta="Local Guide · 2 weeks ago", text="Have used Florida State Tree & Landscaping several times.  Harley Roth, Certified Arborist and his team did exceptional work trimming trees and bushes.  I've used them to remove five palms and three pine trees over the years and each time his knowledge and experience really paid off for this homeowner.  Great work and great results.",
      pull="Each time his knowledge and experience really paid off for this homeowner."),
 dict(name="Brent Cleveland", meta="3 months ago", text="They showed up with plenty of notice and got right to work trimming the tree above our home. Crew was very careful with the branches being cut above our garage so no damage was done to roof. Couldn\u2019t beat the great price I was given when other companies were outrageous on just trimming. We are definitely using Florida State Tree Trimming for all other jobs in the future.",
      pull="Crew was very careful with the branches being cut above our garage so no damage was done to roof."),
 dict(name="Tim & Jackie Blomlie", meta="8 months ago", text="Harley did a fantastic job. They were on time and stayed late to finish getting all the debris up. They also went above and beyond and took other tree debris that I had laying around. Their pricing was the best from all the estimates I got, I would definitely use them again for any tree work that I have.",
      pull="They were on time and stayed late to finish getting all the debris up."),
 dict(name="David Allsworth", meta="2 months ago", text="They did a great job trimming branches from over the house and lanai / They pruned the other trees and blew debris off the house and gutters / Highly recommended",
      pull="They pruned the other trees and blew debris off the house and gutters."),
 dict(name="Ivette Tobenas", meta="Local Guide · 2 months ago", excerpt=True, text="We are so grateful to Harley for coming out so quickly to take down a tree on our property. He responded immediately, got the job done right away, and was extremely professional from start to finish. He did an excellent job\u2026",
      pull="He responded immediately, got the job done right away, and was extremely professional from start to finish."),
]
SNIPPETS = ["Great service and pricing.", "These guys never quit and do a fantastic job at a great price!!", "Gave us ideas of what to plant in place of them very knowledgeable person."]

# services: key, title, short, long, photo, alt, tag(for gallery filter)
SVC = [
 ('removal','Tree Removal','Dead, leaning or unwanted trees taken down in sections and hauled off.',
  'From big pines to palms, we take trees down safely in controlled sections, using an aerial lift where the job calls for it, and haul the wood and brush away.',
  'f16','Aerial lift and tractor working on a tall tree trunk being removed in sections'),
 ('trimming','Tree Trimming & Pruning','Limbs lifted off roofs, garages and lanais, canopies shaped and thinned.',
  'Branches hanging over the house, garage or lanai come off carefully, and the rest of the tree gets pruned to look right. Customers mention we even blow the debris off the roof and gutters.',
  'f05','Aerial lift bucket raised into tall trees beside a shed, trimming near overhead lines'),
 ('stumps','Stump Grinding','Stumps ground down so the lawn can grow back.',
  'Once a tree is down, the stump grinder chews the stump below grade so you can replant, lay sod or just mow over it.',
  'f01','Crew member in a safety helmet running a yellow stump grinder in a front yard'),
 ('storm','Storm Cleanup & Emergency Tree Work','Hazardous and fallen trees cleared after a storm.',
  'After a hurricane we cut hazardous trees, remove fallen ones and haul away damaged debris. We\u2019ve traveled as far as Navarre, Florida to help homeowners after a storm.',
  'g02','Aerial lift up among tall oaks during a large removal, with brush piles and a tracked loader below'),
 ('assess','Tree Assessments','Not sure if a tree should stay or go? We\u2019ll take a look.',
  'We\u2019ll look at the tree with you, talk through trimming versus removal, and give you an honest free estimate. One customer said we even gave ideas on what to plant in place of the trees.',
  'f09','A full, leafy shade tree in a front yard in summer'),
 ('landscape','Landscaping','Beds, sod, rock borders and palms for a finished yard.',
  'Full landscaping to finish the job: fresh sod, planting beds, rock borders and palm care, so the yard looks better than before the trees came down.',
  'f13','Freshly laid sod in the front lawn of a home'),
]

CAP = {  # gallery captions (descriptive only) and filter tags
 'f04':("Aerial lift working a moss-hung live oak", 'trimming'),
 'f16':("Taking a tall trunk down in sections", 'removal'),
 'g02':("Big removal job, lift up in the oaks", 'removal'),
 'f10':("Trunk down to a stub, brush and chips around it", 'removal'),
 'f15':("Lift trailer set up beside a tall snag", 'removal'),
 'f05':("Bucket lift up near the lines", 'trimming'),
 'f08':("Working up through tall pines", 'trimming'),
 'f09':("Big shade tree on a front-yard job", 'trimming'),
 'f03':("Fresh-cut rounds from a removal", 'stumps'),
 'f01':("Stump grinder on the job", 'stumps'),
 'f11':("Beds, palms and big shade trees", 'landscape'),
 'f12':("Palm set in a new rock-ringed bed", 'landscape'),
 'f13':("Fresh sod laid out front", 'landscape'),
 'g01':("Queen palms in a front yard", 'landscape'),
}
