package com.darkness.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.result.view.ViewResolver;
import org.springframework.web.servlet.config.annotation.ResourceHandlerRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurerAdapter;
import org.thymeleaf.spring5.SpringTemplateEngine;
import org.thymeleaf.spring5.view.ThymeleafViewResolver;
import org.thymeleaf.templateresolver.ClassLoaderTemplateResolver;

import com.darkness.utils.methods;



@Configuration
public class configApplication<config> 
{

    // ##################################################################################################
    // method Bean
    // ##################################################################################################

    @Bean
    public methods methods() 
    {
        methods methods = new methods();

        return methods;
    }
    
    /*@SuppressWarnings("deprecation")
	@Component
    class WebConfigurer extends WebMvcConfigurerAdapter {
        @Override
        public void addResourceHandlers(ResourceHandlerRegistry registry) {
             registry.addResourceHandler("/ext/**").addResourceLocations("file:/static/");
        }

    }
 
    // ##################################################################################################
    // method Bean
    // ##################################################################################################

   /* @Bean
    public ViewResolver viewResolver()
    {
      ClassLoaderTemplateResolver templateResolver = new ClassLoaderTemplateResolver();
      templateResolver.setTemplateMode("XHTML");
      templateResolver.setPrefix("views/");
      templateResolver.setSuffix(".html");

      SpringTemplateEngine engine = new SpringTemplateEngine();
      engine.setTemplateResolver(templateResolver);

      ThymeleafViewResolver viewResolver = new ThymeleafViewResolver();
      viewResolver.setTemplateEngine(engine);
      return (ViewResolver) viewResolver;
    }*/


}