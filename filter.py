import calendar
import json
import re
from pprint import pprint # For debugging purposes

def courseToTime(course):
    times = []
    for lecture in course["lectures"]:
        for time in lecture["times"]:
            if time["days"] == None or time["begin"] == None:
                return []
            times.append((tuple(time["days"]), (time["begin"], time["end"])))
    return times

def timeKey(t):
    hr = int(t[:2]) % 12
    mn = int(t[3:5])
    if t.endswith("PM"):
        hr += 12
    return 60*hr + mn

def timeRangeKey(t):
    return timeKey(t[0])*60 + timeKey(t[1])

def createWeek(courses):
    week = dict([(x, {}) for x in range(7)])
    for num in sorted(courses):
        times = courseToTime(courses[num])
        for time in times:
            days, hours = time
            for day in days:
                try:
                    week[day][hours].append(num)
                except:
                    week[day][hours] = [num]
    return week

def filterWeekByDay(week, days):
    return {day:week[day] for day in week if day in days}

def timeRangeEnclosed(timeRange, start, end):
    return timeKey(timeRange[0]) > timeKey(start) and timeKey(timeRange[1]) < timeKey(end)

def filterWeekByTime(week, start, end):
    filtered = {}
    for day in week:
        filtered[day] = {}
        for time in week[day]:
            if timeRangeEnclosed(time, start, end):
                try:
                    filtered[day][time].append(week[day][time])
                except:
                    filtered[day][time] = week[day][time]
    return filtered

def pprintWeek(week, courses):
    for day in week:
        print(calendar.day_name[(day+6)%7] + ":")
        for time in sorted(week[day], key=timeRangeKey):
            print(" " * 4 + "-".join(time))
            for course in week[day][time]:
                print(" " * 8 + course, courses[course]["name"])

tepperBreadthText = """First-Year requirements
Units
76-101	Interpretation and Argument	9
79-104	Global Histories	9
Distributional Requirements
CATEGORY 1: SCIENCE & TECHNOLOGY. This requirement seeks to engage students in both exposure to substance, and the experience of, methods in science and technology through courses drawn from the natural and physical sciences, computer science, and engineering.
03-121	Modern Biology	9
03-132	Basic Science to Modern Medicine	9
09-103	Atoms, Molecules and Chemical Change	9
09-105	Introduction to Modern Chemistry I	10
33-104	Experimental Physics	9
33-106	Physics I for Engineering Students	12
33-111	Physics I for Science Students	12
33-115	Physics for Future Presidents	9
33-114	Physics of Musical Sound	9
33-124	Introduction to Astronomy	9
33-131	Matter and Interaction I	12
15-110	Principles of Computing	10
15-112	Fundamentals of Programming and Computer Science	12
15-122	Principles of Imperative Computation	10
06-100	Introduction to Chemical Engineering	12
12-100	Introduction to Civil and Environmental Engineering	12
18-100	Introduction to Electrical and Computer Engineering	12
19-101	Introduction to Engineering and Public Policy	12
19-424	Energy and the Environment	9
24-101	Fundamentals of Mechanical Engineering	12
27-052	Introduction to NanoScience and Technology	9
27-100	Engineering the Materials of the Future	12
42-101	Introduction to Biomedical Engineering	12
CATEGORY 2: COGNITION, CHOICE, AND BEHAVIOR. This requirement explores the process of thinking, decision making, and behavior in the context of the individual.
80-100	Introduction to Philosophy	9
80-130	Introduction to Ethics	9
80-150	Nature of Reason	9
80-242	Conflict and Dispute Resolution	9
80-270	Philosophy of Mind	9
80-271	Philosophy and Psychology	9
80-275	Metaphysics	9
80-230	Ethical Theory	9
85-102	Introduction to Psychology	9
85-211	Cognitive Psychology	9
85-221	Principles of Child Development	9
85-241	Social Psychology	9
85-251	Personality	9
85-261	Abnormal Psychology	9
88-120	Reason, Passion and Cognition	9
CATEGORY 3: POLITICAL AND SOCIAL INSTITUTIONS. This requirement presents courses that analyze, through model-based reasoning, the processes by which institutions organize individual preferences and actions into collective outcomes. Choices draw upon such disciplines as political science, history, and policy analysis.
19-101	Introduction to Engineering and Public Policy	12
79-231	American Foreign Policy: 1945-Present	9
79-300	History of American Public Policy	9
79-330	Medicine and Society	9
79-338	History of Education in America	9
84-104	Decision Processes in American Political Institutions	9
84-275	Comparative Politics	9
84-362	Diplomacy and Statecraft	9
84-326	Theories of International Relations	9
84-366	Presidential Politics: So, You Want to Be President of the United States	9
88-220	Policy Analysis I	9
CATEGORY 4: CREATIVE PRODUCTION & REFLECTION. These courses foster creativity and provide exposure to artistic and intellectual products such as drama, literature, design, music, expository writing, and foreign languages. It also seeks to stimulate critical reflection on the process of creating, and inquiry into why one chooses certain kinds of creative productions.
48-095	Spatial Concepts for Non-Architects I	Var.
51-231	Calligraphy I	9
51-261	Communication Design Fundamentals: Design for Interactions for Communications	9
51-264	Product Design Fundamentals: Design for Interactions for Products	9
54-163	Production for Non Majors	6
54-191	Acting for Non-Majors	9
62-141	Black and White Photography I	10
62-142	Digital Photography I	10
62-102	Modern Dance Workshop	6
Any language course in the Department of Modern Languages (82-xxx) will satisfy this category.
CATEGORY 5: CULTURAL ANALYSIS. This requirement fosters deeper understanding of the role cultures play in shaping individual and social behaviors. Most courses in the Department of History (79-2xx or higher) and any language study or cultural study course in the Department of Modern Languages will satisfy this requirement. The following are examples of commonly chosen courses.
79-201	Introduction to Anthropology	9
79-205	20th/21st Century Europe	9
79-240	Development of American Culture	9
79-241	African American History: Africa to the Civil War	9
79-255	Irish History	6
79-262	Modern China: From the Birth of Mao ... to Now	9
79-275	Introduction to Global Studies	9
79-302	Drone Warfare and Killer Robots: Ethics, Law, Politics, and Strategy	6
79-303	Pittsburgh and the Transformation of Modern Urban America	6
79-305	Moneyball Nation: Data in American Life	9
79-345	Roots of Rock & Roll
"""

if __name__ == "__main__":
    tepperBreadth = set(re.findall(r"\d\d-\d\d\d", tepperBreadthText))

    with open("f17.json") as f: # Generated using CMU Course API
        c = json.load(f)

    courses = c["courses"]
    filtered = {num:courses[num] for num in courses if num in tepperBreadth}
    week = createWeek(filtered)
    pprintWeek(week, filtered)

    # Example code for time filtering, which I implemented before noticing SIO did the same already
    # days = (2, 4)
    # start = "08:00AM"
    # end = "12:00PM"
    #
    # filtered = filterWeekByDay(week, days)
    # pprintWeek(filtered, courses)
    #
    # filtered = filterWeekByTime(filtered, start, end)
    # pprintWeek(filtered, courses)
