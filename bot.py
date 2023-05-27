import psychxchange as psychxchange

def robotInfo():
    print("\n")
    print("       ===============================================================")
    print("       =               WELCOME TO Job SCRAPER :-)                    =")
    print("       = ----------------------------------------------------------- =")
    print("       = VERSION: 1.00                                               =")
    print("       = DATE: May 27, 2023                                        =")
    print("       = DEVELOPER : MUHAMMAD AHMAD                                  =")
    print("       = heremuhammadahmad@gmail.com                                 =")
    print("       ===============================================================")
    print("\n\n")
    print("-------->>> JOB SCRAPER START... :-)\n")


def menu():
    print("FOLLOWING SITES ARE AVAILABLE TO SCRAPES!\n")
    print("1: PSYCHXCHANGE.COM.AU")


if __name__ == '__main__':
    start = True
    robotInfo()
    while start:
        menu()
        scrapeSite = int(input("\n-> SELECT SITE TO SCRAPE: "))

        if scrapeSite == 1:
            jobsLinks = psychxchange.getJobLinks()
            if len(jobsLinks) > 0:
                psychxchange.scrapeJob(jobsLinks)
            else:
                print("No Job Found!")
        isRun = input("\nDO YOU WANT TO RUN AGAIN THEN WRITE (yes)? TO CANCEL PRESS ANY KEYWORD: ")

        if isRun == 'yes':
            pass
        else:
            start = False
               
               



