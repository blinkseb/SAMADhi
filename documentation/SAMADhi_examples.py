import SAMADhi

# Example method to generate a dictionary relating PAT name and luminosity
# This version is optimized and only load the needed columns. 
# We also do an implicit join between dataset and sample.
def getPATlumi(sampletype=u"mc"): # can be u"mc", u"data", u"%"
  dbstore = SAMADhi.DbStore()
  pattuples = dbstore.find(SAMADhi.Sample,SAMADhi.Dataset.dataset_id==SAMADhi.Sample.source_dataset_id,
                           (SAMADhi.Sample.sampletype==u"PAT") & (SAMADhi.Dataset.datatype.like(sampletype)))
  luminosities = pattuples.values(SAMADhi.Sample.name, SAMADhi.Sample.luminosity)
  dictionary = {}
  for name,lumi in luminosities:
    dictionary[name]=lumi
  return dictionary

# Example method to access a PAT based on the path and access results and dataset
def getPAT(path=u"%"):
  dbstore = SAMADhi.DbStore()
  pattuples = dbstore.find(SAMADhi.Sample,(SAMADhi.Sample.sampletype==u"PAT") & (SAMADhi.Sample.path.like(path)))
  for pattuple in pattuples:
    print pattuple
    print "results obtained from that sample:"
    for res in pattuple.results:
      print res
    print "source dataset:"
    print pattuple.source_dataset

# Example to access the weight of an event
def getWeights(dataset, run, event):
  dbstore = SAMADhi.DbStore()
  event = dbstore.find(SAMADhi.Event,(SAMADhi.Event.run_number==run) & (SAMADhi.Event.event_number==event) & (SAMADhi.Event.dataset_id==dataset))
  theEvent = event.one()
  for w in theEvent.weights:
    print "weight for process %s (version %d): %g+/-%g"%(w.process.name,w.version,w.value,w.uncertainty)

# Get a single event weight
# Note that I think that the getWeights above will be faster than n times this method.
def getWeight(dataset, run, event, process, version=None):
  dbstore = SAMADhi.DbStore()
  weight = dbstore.find(SAMADhi.Weight, SAMADhi.Weight.event_id==SAMADhi.Event.event_id, 
                        (SAMADhi.Event.run_number==run) & (SAMADhi.Event.event_number==event) & (SAMADhi.Event.dataset_id==dataset) &
                        (SAMADhi.Weight.madweight_process==process))
  if version is None: # take the most recent
    w = weight.order_by(SAMADhi.Weight.version).last()
  else:
    w = weight.find(SAMADhi.Weight.version==version).one()
  return (w.value, w.uncertainty)

# In the example above, you need the dataset id. It can be obtained this way
# It could be combined in a complex query, but typically you will get this once
# and avoid doing the joined query for every event.
def dataset_id(dataset=None, pat=None):
  dbstore = SAMADhi.DbStore()
  if dataset is None and pat is not None:
    dset = dbstore.find(SAMADhi.Dataset,SAMADhi.Dataset.dataset_id==SAMADhi.Sample.source_dataset_id,SAMADhi.Sample.name==pat)
  elif dataset is not None and pat is None:
    dset = dbstore.find(SAMADhi.Dataset,SAMADhi.Dataset.name==dataset)
  else:
    return 0
  return dset.one().dataset_id
  
