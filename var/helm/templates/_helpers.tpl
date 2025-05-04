
{{/* Common labels */}}
{{ define "common.labels" }}
app: mpafastapi
version: {{ .Chart.AppVersion }}
app.kubernetes.io/part-of: mpafastapi
app.kubernetes.io/version: {{ .Chart.AppVersion }}
{{ end }}
