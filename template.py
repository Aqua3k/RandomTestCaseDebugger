######################################
# result.txt用
noError = 'No error occured.'
ErrorOccured = '{errNum} error occured.'
errorMessage = '{fileName} {progName} \n{errorMessage}'

noDifference = 'No difference.'
differenceFound = '{diffNum} difference found.'

######################################
# THML関連
HTMLLinkStr = '<a href="{path}">{string}</a><br>'

cssLink = '<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/kognise/water.css@latest/dist/light.min.css">'

Table = '<table border="{border}">{body}</table>'
TableHeader = '<tr><th>{text1}</th><th bgcolor={color}>{text2}</th><th>{text3}</th></tr>'
TableBody   = '<tr><td>{text1}</td><td bgcolor={color}>{text2}</td><td>{text3}</th></td>'
HTMLFont = '<font size="{size}" >{text}</font>'

HTMLText = '''
<html>
<head>
<meta charset="utf-8">
<title>{title}</title>
</head>
<body>
{body}
</body>
</html>
'''
