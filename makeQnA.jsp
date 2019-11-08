<%@ page language="java" contentType="application/json; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ page import="java.io.IOException"%>
<%@ page import="java.io.BufferedReader"%>
<%@ page import="java.io.InputStreamReader"%>
<%@ page import="java.io.File" %>
<%@ page import="java.io.FileReader" %>

<%
	String category = request.getParameter("category");
	String keyword = request.getParameter("keyword");
	String s;
	Runtime rt = Runtime.getRuntime();
	Process p;
	
	System.out.println(category);
	System.out.println(keyword);
	
	try {
		p = rt.exec("Python C:/Users/user/eclipse-workspace/QnA/WebContent/Content/makeQuestion.py " + category + " " + keyword);
		BufferedReader stdInput = new BufferedReader(new InputStreamReader(p.getInputStream()));
		BufferedReader stdError = new BufferedReader(new InputStreamReader(p.getErrorStream()));
		while((s=stdInput.readLine()) != null) {
			System.out.println(s);
		}
		while((s = stdError.readLine()) != null) {
			System.out.println(s);
		}
		File file = new File("C:/Users/user/Desktop/test.json");
		FileReader fr = new FileReader(file);
		BufferedReader br = new BufferedReader(fr);
		String json = br.readLine();
		out.print(json);
		System.out.println(json);
		System.out.println(new File("").getAbsolutePath());
	} catch (IOException e) {
		e.printStackTrace();
		out.print("{ \"result\": 0 }");
		System.out.println("F");
	}

%>