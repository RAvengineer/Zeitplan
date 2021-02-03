from datefinder import find_dates
from datetime import datetime,timedelta

class ParseTimeTable():
    '''
    Parses the time-table provided in V-TOP and \n
    returns list of lectures with list of details of respective lecture.\n
    Details include:\n
    course,faculty,slot,course_type,category,class_number,LTPJC\n
    All of this will be parsed from raw text copied from the Time-Table page on V-TOP
    '''
    def __init__(self):
        '''
        Constructor for ParseTimeTable\n
        Initializes:
            number_of_cols=14
            "start_times" for each lecture
            "slot_details" as the day and timing they belong to
            "days" from Monday to Sunday
        '''
        self.number_of_cols = 14
        self.thoery_duration = 50
        self.lab_duration = 100
        self.start_times = (
            # '08:00', '08:55', '09:50', '10:45', '11:40', '12:35', '14:00', '14:55', '15:50', '16:50', '17:40', '18:35',
            '08:00 AM', '08:55 AM', '09:50 AM', '10:45 AM', '11:40 AM', '12:35 PM', '02:00 PM', '02:55 PM', '03:50 PM', '04:45 PM', '05:40 PM', '06:35 PM',
        )
        # day_index: 0-6 where 0 => Monday
        # "slot":[[day_index,start_time_index],]
        self.slot_details = {
            # Theory
            "A1":[[0,0],[2,1]],"A2":[[0,5],[2,6]],
            "B1":[[1,0],[3,1]],"B2":[[1,5],[3,6]],
            "C1":[[2,0],[4,1]],"C2":[[2,5],[4,6]],
            "D1":[[3,0],[0,2]],"D2":[[3,5],[0,7]],
            "E1":[[4,0],[1,2]],"E2":[[4,5],[1,7]],
            "F1":[[0,1],[2,2]],"F2":[[0,6],[2,7]],
            "G1":[[1,1],[3,2]],"G2":[[1,6],[3,7]],
            "TA1":[[4,2]],"TA2":[[4,7]],
            "TB1":[[0,3]],"TB2":[[0,8]],
            "TC1":[[1,3]],"TC2":[[1,8]],
            "TD1":[[2,3]],"TD2":[[2,8]],
            "TE1":[[3,3]],"TE2":[[3,8]],
            "TF1":[[4,3]],"TF2":[[4,8]],
            "TG1":[[0,4]],"TG2":[[0,9]],
            "TAA1":[[1,4]],"TAA2":[[1,9]],
            "TBB1":[[2,4]],"TBB2":[[2,9]], # I know TBB1 is Extramural, I'm just playing safe!
            "TCC1":[[3,4]],"TCC2":[[3,9]],
            "TDD1":[[4,4]],"TDD2":[[4,9]],
            "V8":[[5,0]],"V10":[[6,0]],
            "W21":[[5,8],[6,8]],"W22":[[5,9],[6,9]],
            "X11":[[5,1],[6,3]],"X12":[[5,2],[6,4]],
            "Y11":[[5,3],[6,1]],"Y12":[[5,4],[6,2]],
            "X21":[[5,5],[6,7]],"Y21":[[6,5],[5,7]],
            "Z21":[[5,6],[6,6]],
            # Lab
            "L1+L2":[[0,0]],"L31+L32":[[0,5]],
            "L3+L4":[[0,2]],"L33+L34":[[0,7]],
            "L5+L6":[[0,4]],"L35+L36":[[0,9]],
            "L7+L8":[[1,0]],"L37+L38":[[1,5]],
            "L9+L10":[[1,2]],"L39+L40":[[1,7]],
            "L11+L12":[[1,4]],"L41+L42":[[1,9]],
            "L13+L14":[[2,0]],"L43+L44":[[2,5]],
            "L15+L16":[[2,2]],"L45+L46":[[2,7]],
            "L17+L18":[[2,4]],"L47+L48":[[2,9]],
            "L19+L20":[[3,0]],"L49+L50":[[3,5]],
            "L21+L22":[[3,2]],"L51+L52":[[3,7]],
            "L23+L24":[[3,4]],"L53+L54":[[3,9]],
            "L25+L26":[[4,0]],"L55+L56":[[4,5]],
            "L27+L28":[[4,2]],"L57+L58":[[4,7]],
            "L29+L30":[[4,4]],"L59+L60":[[4,9]],
            "L71+L72":[[5,0]],"L77+L78":[[5,5]],
            "L73+L74":[[5,2]],"L79+L80":[[5,7]],
            "L75+L76":[[5,4]],"L81+L82":[[5,9]],
            "L83+L84":[[6,0]],"L89+L90":[[6,5]],
            "L85+L86":[[6,2]],"L91+L92":[[6,7]],
            "L87+L88":[[6,4]],"L93+L94":[[6,9]],           
        }
        self.days = ['']*7        
    
    
    def addDatesToDaysList(self, date):
        '''
        Replaces the dates that belongs to their respective days\n
        with the items in the list "days"\n
        Parameters:
            date: str
        Returns:
            -1 if Error, otherwise 0
        '''
        try:
            dt = list(find_dates(date))
        except Exception as e:
            print(str(e))
            return -1
        if(len(dt)==0):
            print("Error in ParseTimeTable.py addDatesToDaysList() function:\nlength of possible dates list = 0")
            return -1
        dt = dt[0]
        self.days = ['']*7
        for i in range(7):
            self.days[dt.weekday()] = dt.strftime("%d %B %Y")
            dt += timedelta(days=1)
        return 0


    def parseTT(self, data):
        '''
        Converts Raw data provided as text to a list of lectures\n
        with details like slot,title,location,description,duration,popup\n
        Parameters:
            data: str
        Returns:
            list(list)
        '''
        data = list(filter(lambda a: a != '',[x.rstrip() for x in data.split('\n')]))
        """
        data -> '1', 'General (Semester)', 'STS2102 - Enhancing Problem Solving Skills - Soft Skill', '0 0 0 0 1', 'University Core', 'Regular', 'CH2019205000291', 'F1+TF1', 'AB1-408', 'SMART (APT) - ACAD', '01-Nov-2019 14:06', '02-Nov-2019', '- Manual', 'Registered and Approved', '2', ...
        """
        parsedTimeTable = list()
        for i in range(len(data)//self.number_of_cols):
            course_code, course, course_type = data[2].split(" - ")
            LTPJC = data[3]
            category = data[4]
            class_number = data[6]
            slots = [data[7]]
            if(course_type!="Embedded Lab"):
                slots = data[7].split('+')
            venue = data[8]
            faculty = data[9]
            data = data[self.number_of_cols:]
            # Avoid Projects as they have the same slot as Theory and causes problem later
            # LazyProgrammer :P
            if(course_type=="Embedded Project"):
                continue
            for slot in slots:
                title = course_code
                location = venue
                description = "\n".join([course,faculty,"Slot: "+slot,course_type,category,"Class Number: "+class_number,"L T P J C",LTPJC,])
                duration = self.thoery_duration
                if(slot[0]=='L'):
                    duration = self.lab_duration
                popup = duration//10
                parsedTimeTable.append([slot,title,location,description,duration,popup])
        return parsedTimeTable
    

    def convertTTtoEvents(self,data,date):
        '''
        Converts the Time-Table provided in Raw Text to \n
        list of Events, ready to be added as Events using Calendar API\n
        Format of events:
            datetime, title, location, description, duration, popup
        Parameters:
            data: str :- Raw Text Time-Table
            date: str :- Start Date for the Events to be added
        Returns:
            list(list)
        '''
        try:
            if(self.addDatesToDaysList(date)==-1):
                raise(Exception("Error in addDatesToDaysList() function"))
            parsed_data = list()
            parsedTimeTable = self.parseTT(data)
            for lecture in parsedTimeTable:
                for indices in self.slot_details[lecture[0]]:
                    start_time = list(find_dates(self.days[indices[0]]+' '+self.start_times[indices[1]]))
                    if(len(start_time)>0):
                        start_time = start_time[0]
                    else:
                        raise(Exception("Couldn't find match for start_time"))
                    parsed_data.append([start_time]+lecture[1:])
            return parsed_data
        except Exception as e:
            raise(Exception("Error in ParseTimeTable.py convertTTtoEvents():"+str(e)))
