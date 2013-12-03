from time import gmtime, strftime, sleep
from report import get_release_detail_info,get_preb_report_url,get_preb_report_info

if __name__ == '__main__':
    print strftime("%Y-%m-%d-%H:%M:%S", gmtime())
    get_release_detail_info('RELDB00018711') 
    print strftime("%Y-%m-%d-%H:%M:%S", gmtime())
    prep_report_url = get_preb_report_url()
    print strftime("%Y-%m-%d-%H:%M:%S", gmtime())
    get_preb_report_info(prep_report_url)
    print strftime("%Y-%m-%d-%H:%M:%S", gmtime())
