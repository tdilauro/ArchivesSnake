from .common import vcr
from asnake.aspace import ASpace, JSONModelRelation, JSONModelObject
import os

conf_file = None

def setup():
    '''Point ASNAKE_CONFIG_FILE at non-extant path so local config DEF HAPPENS even if you have a config'''
    try:
        conf_file = os.environ.pop('ASNAKE_CONFIG_FILE')
    except: pass
    os.environ['ASNAKE_CONFIG_FILE'] = "NONSENSEFILETHATDOESNOTEXIST"

@vcr.use_cassette
def test_fetch():
    aspace = ASpace()
    assert isinstance(aspace.repositories, JSONModelRelation)
    resolved = list(aspace.repositories)
    assert resolved[0].jsonmodel_type == "repository"
    repo_id = resolved[0].uri.split("/")[-1]
    assert isinstance(aspace.repositories(repo_id), JSONModelObject)

def teardown():
    '''Undo the thing from setup'''
    if conf_file:
        os.environ['ASNAKE_CONFIG_FILE'] = conf_file
    else:
        os.environ.pop('ASNAKE_CONFIG_FILE')