from datetime import datetime, date


def isObsolete(lastUpdated: datetime) -> bool:
    return (date.today() - lastUpdated.date()).days > 3 * 365

#    As an extra ...
#    Tries to extract theme info from the description
#    MUST be called after the description is set!
def bestEffortTheme(res):
    if not res['descriptionText']:
        return
    if 'theme' not in res: res['theme'] = []
    if "XMPP" in res['descriptionText']: res['theme'].append("XMPP")
    if "android" in res['descriptionText'].lower(): res['theme'].append("Android")
    if "vim" in res['descriptionText'].lower(): res['theme'].append("Vim")
    if "git" in res['descriptionText'].lower(): res['theme'].append("Git")
    if "ledger" in res['descriptionText'].lower(): res['theme'].append("Ledger")
    if "time" in res['descriptionText'].lower(): res['theme'].append("Time")
    if "web" in res['descriptionText'].lower(): res['theme'].append("Web")
    if "mail" in res['descriptionText'].lower() or "smtp" in res['descriptionText'].lower() :
        res['theme'].append("Mail")
    if "os x" in res['descriptionText'].lower() or "osx" in res['descriptionText'].lower() :
        res['theme'].append("OSX")
    if "GUI" in res['descriptionText']\
          or "GTK" in res['descriptionText']\
          or "graphic" in res['descriptionText'].lower() :
        res['theme'].append("GUI")

