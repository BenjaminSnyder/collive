import diff_match_patch as dmp_module # python3.9 -m pip install diff_match_patch
import requests

from database.db import Database

global hashify_url
hashify_url = 'api.hashify.net/hash/md5/'


# handles creating diffs and giving the hashes
class document_util:

    @staticmethod
    def update_document(db: Database, doc_id: str,
                        local_revision_hash: str, content: str) -> str:
        '''
        Given a document_id, local document hash, and new content
        it updates the document with the changes from their local revision
        '''

        # Make some call to the database to get the content based on the hash
        '''
        old_content = Document.get_revision(doc_id, local_revision_hash)
        '''

        # Create diff_match_patch object
        dmp = dmp_module.diff_match_patch()

        # set max diff calculate time to 100 milliseconds
        dmp.Diff_Timeout = 0.1

        # Use this revision to create a diff between
        # their local content and their old local content
        diff = dmp.diff_main(old_content, content)

        # Clean up diff to make it more human readable
        dmp.diff_cleanupSemantic(diff)

        # Create list of patches based on the diff
        patches = dmp.patch_make(diff)

        # Get the most recent revision for a document
        current_revision = db.get_most_recent_revision(doc_id)

        # Apply this patch (changes from their version to new content)
        # to the current revision
        # @TODO: Handle weird behavior with unapplied patches
        updated_text, results = dmp.patch_apply(patches, current_revision)
        return updated_text

    @staticmethod
    def create_hash(content: str) -> str:
        '''Sends the content to hashify to get a hash for the '''
        req = requests.get(hashify_url + '?value=' + content)
        return req.json()['Digest']
