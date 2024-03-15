def generateHTML(matches_data, recipient_name, recipient_teams):
    html = f"<div><p>Hello, {recipient_name}!</p><p>Your teams: {', '.join(recipient_teams)}</p>"
    for team, match_set in zip(recipient_teams, matches_data):
        html += f"<h2>{team}</h2>"
        for match in match_set:
            html += "<div>"
            html += f"<h3>{match['hometeam']} ({match['homerank']}) vs {match['awayteam']} ({match['awayrank']})</h3>"
            html += f"<p>{match['homeform']} {match['awayform']}</p>"
            html += f"<p>{match['league']}</p>"
            html += f"<p>Stadium: {match['venue']}</p>"
            html += f"<p>Date: {match['date'].strftime('%d/%m/%Y')}, {match['time']}</p>"
            html += "<hr></div>"
    html += "</div>"

    with open("match_info.html", "w") as file:
        file.write(html)

    print("Match information has been saved to match_info.html")