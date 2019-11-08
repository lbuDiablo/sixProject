<%@ page language="java" contentType="application/json; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ page import="java.io.IOException"%>
<%@ page import="java.io.BufferedReader"%>
<%@ page import="java.io.InputStreamReader"%>
<%@ page import="java.io.File" %>
<%@ page import="java.io.BufferedWriter" %>
<%@ page import="java.io.OutputStreamWriter" %>
<%@ page import="java.io.FileOutputStream" %>

<%
	String category = request.getParameter("category");
	String keyword = request.getParameter("keyword");
	String paragraph = request.getParameter("paragraph");
	String s;
	Runtime rt = Runtime.getRuntime();
	Process p;
	
	System.out.println(category);
	System.out.println(keyword);
	System.out.println(paragraph);
	try {
		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(new FileOutputStream("paragraph.txt"),"UTF8"));
		bw.write(paragraph);
		bw.close();
		System.out.println(new File("").getAbsolutePath());
		p = rt.exec("Python C:/Users/user/eclipse-workspace/QnA/WebContent/Content/collect.py "+category+" "+keyword);
		//p = rt.exec("Python3 collect.py "+category+" "+keyword);
		BufferedReader stdInput = new BufferedReader(new InputStreamReader(p.getInputStream()));
		BufferedReader stdError = new BufferedReader(new InputStreamReader(p.getErrorStream()));
		while((s=stdInput.readLine()) != null) {
			System.out.println(s);
		}
		while((s = stdError.readLine()) != null) {
			System.out.println(s);
		}
		out.print("{ \"result\": 1 }");
		System.out.println("S");
	} catch (IOException e) {
		e.printStackTrace();
		out.print("{ \"result\": 0 }");
		System.out.println("F");
	}


%>