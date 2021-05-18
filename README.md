# Time Traveling 
spring boot application

https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/#production-ready-endpoints
https://www.baeldung.com/spring-boot-actuators
<!-- [INFO] Scanning for projects...
[WARNING] 
[WARNING] Some problems were encountered while building the effective model for com.run:darkness:jar:.001
[WARNING] 'dependencies.dependency.(groupId:artifactId:type:classifier)' must be unique: org.springframework.boot:spring-boot-starter-web:jar -> duplicate declaration of version (?) @ line 63, column 21
[WARNING] 'dependencies.dependency.(groupId:artifactId:type:classifier)' must be unique: org.springframework.boot:spring-boot-starter-test:jar -> duplicate declaration of version (?) @ line 72, column 21
[WARNING] 
[WARNING] It is highly recommended to fix these problems because they threaten the stability of your build.
[WARNING] 
[WARNING] For this reason, future Maven versions might no longer support building such malformed projects.
[WARNING] 
[INFO] 
[INFO] -------------------------< com.run:darkness >-------------------------
[INFO] Building darkness .001
[INFO] --------------------------------[ jar ]---------------------------------
[INFO] 
[INFO] --- maven-clean-plugin:3.1.0:clean (default-clean) @ darkness ---
[INFO] Deleting /home/maestro/git/darkness/target
[INFO] 
[INFO] --- maven-resources-plugin:3.1.0:resources (default-resources) @ darkness ---
[INFO] Using 'UTF-8' encoding to copy filtered resources.
[INFO] Copying 1 resource
[INFO] Copying 8 resources
[INFO] 
[INFO] --- maven-compiler-plugin:3.8.0:compile (default-compile) @ darkness ---
[INFO] Changes detected - recompiling the module!
[INFO] Compiling 19 source files to /home/maestro/git/darkness/target/classes
[INFO] /home/maestro/git/darkness/src/main/java/com/darkness/config/Initialize.java: Some input files use or override a deprecated API.
[INFO] /home/maestro/git/darkness/src/main/java/com/darkness/config/Initialize.java: Recompile with -Xlint:deprecation for details.
[INFO] /home/maestro/git/darkness/src/main/java/com/darkness/utils/methods.java: /home/maestro/git/darkness/src/main/java/com/darkness/utils/methods.java uses unchecked or unsafe operations.
[INFO] /home/maestro/git/darkness/src/main/java/com/darkness/utils/methods.java: Recompile with -Xlint:unchecked for details.
[INFO] 
[INFO] --- maven-resources-plugin:3.1.0:testResources (default-testResources) @ darkness ---
[INFO] Using 'UTF-8' encoding to copy filtered resources.
[INFO] skip non existing resourceDirectory /home/maestro/git/darkness/src/test/resources
[INFO] 
[INFO] --- maven-compiler-plugin:3.8.0:testCompile (default-testCompile) @ darkness ---
[INFO] Changes detected - recompiling the module!
[INFO] Compiling 1 source file to /home/maestro/git/darkness/target/test-classes
[INFO] 
[INFO] --- maven-surefire-plugin:2.22.1:test (default-test) @ darkness ---
[INFO] 
[INFO] -------------------------------------------------------
[INFO]  T E S T S
[INFO] -------------------------------------------------------
[INFO] Running com.darkness.darknessApplicationTests
21:26:47.756 [main] DEBUG org.springframework.test.context.junit4.SpringJUnit4ClassRunner - SpringJUnit4ClassRunner constructor called with [class com.darkness.darknessApplicationTests]
21:26:47.764 [main] DEBUG org.springframework.test.context.BootstrapUtils - Instantiating CacheAwareContextLoaderDelegate from class [org.springframework.test.context.cache.DefaultCacheAwareContextLoaderDelegate]
21:26:47.821 [main] DEBUG org.springframework.test.context.BootstrapUtils - Instantiating BootstrapContext using constructor [public org.springframework.test.context.support.DefaultBootstrapContext(java.lang.Class,org.springframework.test.context.CacheAwareContextLoaderDelegate)]
21:26:47.917 [main] DEBUG org.springframework.test.context.BootstrapUtils - Instantiating TestContextBootstrapper for test class [com.darkness.darknessApplicationTests] from class [org.springframework.boot.test.context.SpringBootTestContextBootstrapper]
21:26:48.246 [main] INFO org.springframework.boot.test.context.SpringBootTestContextBootstrapper - Neither @ContextConfiguration nor @ContextHierarchy found for test class [com.darkness.darknessApplicationTests], using SpringBootContextLoader
21:26:48.380 [main] DEBUG org.springframework.test.context.support.AbstractContextLoader - Did not detect default resource location for test class [com.darkness.darknessApplicationTests]: class path resource [com/darkness/darknessApplicationTests-context.xml] does not exist
21:26:48.442 [main] DEBUG org.springframework.test.context.support.AbstractContextLoader - Did not detect default resource location for test class [com.darkness.darknessApplicationTests]: class path resource [com/darkness/darknessApplicationTestsContext.groovy] does not exist
21:26:48.442 [main] INFO org.springframework.test.context.support.AbstractContextLoader - Could not detect default resource locations for test class [com.darkness.darknessApplicationTests]: no resource found for suffixes {-context.xml, Context.groovy}.
21:26:48.444 [main] INFO org.springframework.test.context.support.AnnotationConfigContextLoaderUtils - Could not detect default configuration classes for test class [com.darkness.darknessApplicationTests]: darknessApplicationTests does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
21:26:48.755 [main] DEBUG org.springframework.test.context.support.ActiveProfilesUtils - Could not find an 'annotation declaring class' for annotation type [org.springframework.test.context.ActiveProfiles] and class [com.darkness.darknessApplicationTests]
21:26:49.265 [main] DEBUG org.springframework.context.annotation.ClassPathScanningCandidateComponentProvider - Identified candidate component class: file [/home/maestro/git/darkness/target/classes/com/darkness/darkness.class]
21:26:49.267 [main] INFO org.springframework.boot.test.context.SpringBootTestContextBootstrapper - Found @SpringBootConfiguration com.darkness.darkness for test class com.darkness.darknessApplicationTests
21:26:49.862 [main] DEBUG org.springframework.boot.test.context.SpringBootTestContextBootstrapper - @TestExecutionListeners is not present for class [com.darkness.darknessApplicationTests]: using defaults.
21:26:49.863 [main] INFO org.springframework.boot.test.context.SpringBootTestContextBootstrapper - Loaded default TestExecutionListener class names from location [META-INF/spring.factories]: [org.springframework.boot.test.mock.mockito.MockitoTestExecutionListener, org.springframework.boot.test.mock.mockito.ResetMocksTestExecutionListener, org.springframework.boot.test.autoconfigure.restdocs.RestDocsTestExecutionListener, org.springframework.boot.test.autoconfigure.web.client.MockRestServiceServerResetTestExecutionListener, org.springframework.boot.test.autoconfigure.web.servlet.MockMvcPrintOnlyOnFailureTestExecutionListener, org.springframework.boot.test.autoconfigure.web.servlet.WebDriverTestExecutionListener, org.springframework.test.context.web.ServletTestExecutionListener, org.springframework.test.context.support.DirtiesContextBeforeModesTestExecutionListener, org.springframework.test.context.support.DependencyInjectionTestExecutionListener, org.springframework.test.context.support.DirtiesContextTestExecutionListener, org.springframework.test.context.transaction.TransactionalTestExecutionListener, org.springframework.test.context.jdbc.SqlScriptsTestExecutionListener]
21:26:49.975 [main] INFO org.springframework.boot.test.context.SpringBootTestContextBootstrapper - Using TestExecutionListeners: [org.springframework.test.context.web.ServletTestExecutionListener@73cd37c0, org.springframework.test.context.support.DirtiesContextBeforeModesTestExecutionListener@21337f7b, org.springframework.boot.test.mock.mockito.MockitoTestExecutionListener@2bb3058, org.springframework.boot.test.autoconfigure.SpringBootDependencyInjectionTestExecutionListener@7a362b6b, org.springframework.test.context.support.DirtiesContextTestExecutionListener@60df60da, org.springframework.test.context.transaction.TransactionalTestExecutionListener@5a2d131d, org.springframework.test.context.jdbc.SqlScriptsTestExecutionListener@14fc1f0, org.springframework.boot.test.mock.mockito.ResetMocksTestExecutionListener@4ae9cfc1, org.springframework.boot.test.autoconfigure.restdocs.RestDocsTestExecutionListener@512baff6, org.springframework.boot.test.autoconfigure.web.client.MockRestServiceServerResetTestExecutionListener@632ceb35, org.springframework.boot.test.autoconfigure.web.servlet.MockMvcPrintOnlyOnFailureTestExecutionListener@1c93f6e1, org.springframework.boot.test.autoconfigure.web.servlet.WebDriverTestExecutionListener@1800a575]
21:26:49.981 [main] DEBUG org.springframework.test.annotation.ProfileValueUtils - Retrieved @ProfileValueSourceConfiguration [null] for test class [com.darkness.darknessApplicationTests]
21:26:49.982 [main] DEBUG org.springframework.test.annotation.ProfileValueUtils - Retrieved ProfileValueSource type [class org.springframework.test.annotation.SystemProfileValueSource] for class [com.darkness.darknessApplicationTests]
21:26:49.993 [main] DEBUG org.springframework.test.annotation.ProfileValueUtils - Retrieved @ProfileValueSourceConfiguration [null] for test class [com.darkness.darknessApplicationTests]
21:26:49.994 [main] DEBUG org.springframework.test.annotation.ProfileValueUtils - Retrieved ProfileValueSource type [class org.springframework.test.annotation.SystemProfileValueSource] for class [com.darkness.darknessApplicationTests]
21:26:50.169 [main] DEBUG org.springframework.test.annotation.ProfileValueUtils - Retrieved @ProfileValueSourceConfiguration [null] for test class [com.darkness.darknessApplicationTests]
21:26:50.170 [main] DEBUG org.springframework.test.annotation.ProfileValueUtils - Retrieved ProfileValueSource type [class org.springframework.test.annotation.SystemProfileValueSource] for class [com.darkness.darknessApplicationTests]
21:26:50.173 [main] DEBUG org.springframework.test.context.support.AbstractDirtiesContextTestExecutionListener - Before test class: context [DefaultTestContext@764faa6 testClass = darknessApplicationTests, testInstance = [null], testMethod = [null], testException = [null], mergedContextConfiguration = [WebMergedContextConfiguration@4c1f22f3 testClass = darknessApplicationTests, locations = '{}', classes = '{class com.darkness.darkness}', contextInitializerClasses = '[]', activeProfiles = '{}', propertySourceLocations = '{}', propertySourceProperties = '{org.springframework.boot.test.context.SpringBootTestContextBootstrapper=true}', contextCustomizers = set[org.springframework.boot.test.context.filter.ExcludeFilterContextCustomizer@741a8937, org.springframework.boot.test.json.DuplicateJsonObjectContextCustomizerFactory$DuplicateJsonObjectContextCustomizer@6fd83fc1, org.springframework.boot.test.mock.mockito.MockitoContextCustomizer@0, org.springframework.boot.test.web.client.TestRestTemplateContextCustomizer@f0da945, org.springframework.boot.test.web.reactive.server.WebTestClientContextCustomizer@66f57048, org.springframework.boot.test.autoconfigure.properties.PropertyMappingContextCustomizer@0, org.springframework.boot.test.autoconfigure.web.servlet.WebDriverContextCustomizerFactory$Customizer@4c1909a3], resourceBasePath = 'src/main/webapp', contextLoader = 'org.springframework.boot.test.context.SpringBootContextLoader', parent = [null]], attributes = map['org.springframework.test.context.web.ServletTestExecutionListener.activateListener' -> true]], class annotated with @DirtiesContext [false] with mode [null].
21:26:50.174 [main] DEBUG org.springframework.test.annotation.ProfileValueUtils - Retrieved @ProfileValueSourceConfiguration [null] for test class [com.darkness.darknessApplicationTests]
21:26:50.174 [main] DEBUG org.springframework.test.annotation.ProfileValueUtils - Retrieved ProfileValueSource type [class org.springframework.test.annotation.SystemProfileValueSource] for class [com.darkness.darknessApplicationTests]
21:26:50.240 [main] DEBUG org.springframework.test.context.support.TestPropertySourceUtils - Adding inlined properties to environment: {spring.jmx.enabled=false, org.springframework.boot.test.context.SpringBootTestContextBootstrapper=true, server.port=-1}

  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/
 :: Spring Boot ::        (v2.1.1.RELEASE)

2018-12-10 21:26:51.730  INFO 5384 --- [           main] c.darkness.darknessApplicationTests  : Starting darknessApplicationTests on slave-one with PID 5384 (started by maestro in /home/maestro/git/darkness)
2018-12-10 21:26:51.731  INFO 5384 --- [           main] c.darkness.darknessApplicationTests  : No active profile set, falling back to default profiles: default
2018-12-10 21:27:10.213  INFO 5384 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Bootstrapping Spring Data repositories in DEFAULT mode.
2018-12-10 21:27:12.338  INFO 5384 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Finished Spring Data repository scanning in 1952ms. Found 5 repository interfaces.
2018-12-10 21:27:18.045  INFO 5384 --- [           main] trationDelegate$BeanPostProcessorChecker : Bean 'org.springframework.ws.config.annotation.DelegatingWsConfiguration' of type [org.springframework.ws.config.annotation.DelegatingWsConfiguration$$EnhancerBySpringCGLIB$$4ffa29b2] is not eligible for getting processed by all BeanPostProcessors (for example: not eligible for auto-proxying)
2018-12-10 21:27:21.088  INFO 5384 --- [           main] .w.s.a.s.AnnotationActionEndpointMapping : Supporting [WS-Addressing August 2004, WS-Addressing 1.0]
2018-12-10 21:27:21.442  INFO 5384 --- [           main] trationDelegate$BeanPostProcessorChecker : Bean 'org.springframework.transaction.annotation.ProxyTransactionManagementConfiguration' of type [org.springframework.transaction.annotation.ProxyTransactionManagementConfiguration$$EnhancerBySpringCGLIB$$ab6264b3] is not eligible for getting processed by all BeanPostProcessors (for example: not eligible for auto-proxying)
2018-12-10 21:27:25.271  INFO 5384 --- [           main] com.zaxxer.hikari.HikariDataSource       : HikariPool-1 - Starting...
2018-12-10 21:27:26.948  INFO 5384 --- [           main] com.zaxxer.hikari.HikariDataSource       : HikariPool-1 - Start completed.
2018-12-10 21:27:28.340  INFO 5384 --- [           main] o.hibernate.jpa.internal.util.LogHelper  : HHH000204: Processing PersistenceUnitInfo [
	name: default
	...]
2018-12-10 21:27:29.200  INFO 5384 --- [           main] org.hibernate.Version                    : HHH000412: Hibernate Core {5.3.7.Final}
2018-12-10 21:27:29.202  INFO 5384 --- [           main] org.hibernate.cfg.Environment            : HHH000206: hibernate.properties not found
2018-12-10 21:27:31.203  INFO 5384 --- [           main] o.hibernate.annotations.common.Version   : HCANN000001: Hibernate Commons Annotations {5.0.4.Final}
2018-12-10 21:27:35.717  INFO 5384 --- [           main] org.hibernate.dialect.Dialect            : HHH000400: Using dialect: org.hibernate.dialect.MariaDB103Dialect
Hibernate: drop table if exists items
Hibernate: drop table if exists map
Hibernate: drop table if exists msg_cache
Hibernate: drop table if exists npc
Hibernate: drop table if exists users
Hibernate: create table items (id integer not null auto_increment, attack integer, defense integer, description varchar(255), name varchar(255), primary key (id)) engine=InnoDB
Hibernate: create table map (id integer not null auto_increment, description varchar(255), items integer, name varchar(255), npcs integer, users integer, primary key (id)) engine=InnoDB
Hibernate: create table msg_cache (id integer not null auto_increment, current_room_status varchar(255), primary key (id)) engine=InnoDB
Hibernate: create table npc (id integer not null auto_increment, attack integer, defense integer, description varchar(255), hp integer, location integer, name varchar(255), primary key (id)) engine=InnoDB
Hibernate: create table users (id integer not null auto_increment, attack integer, defense integer, description varchar(255), exp integer, hp integer, location integer, lvl integer, money integer, name varchar(255), primary key (id)) engine=InnoDB
2018-12-10 21:27:38.668  INFO 5384 --- [           main] o.h.t.schema.internal.SchemaCreatorImpl  : HHH000476: Executing import script 'org.hibernate.tool.schema.internal.exec.ScriptSourceInputNonExistentImpl@3573e19d'
2018-12-10 21:27:38.672  INFO 5384 --- [           main] j.LocalContainerEntityManagerFactoryBean : Initialized JPA EntityManagerFactory for persistence unit 'default'
Hibernate: insert into items (attack, defense, description, name) values (?, ?, ?, ?)
Hibernate: insert into items (attack, defense, description, name) values (?, ?, ?, ?)
mal
Hibernate: insert into npc (attack, defense, description, hp, location, name) values (?, ?, ?, ?, ?, ?)
2018-12-10 21:27:43.110  INFO 5384 --- [           main] o.s.s.concurrent.ThreadPoolTaskExecutor  : Initializing ExecutorService 'applicationTaskExecutor'
2018-12-10 21:27:43.212  WARN 5384 --- [           main] aWebConfiguration$JpaWebMvcConfiguration : spring.jpa.open-in-view is enabled by default. Therefore, database queries may be performed during view rendering. Explicitly configure spring.jpa.open-in-view to disable this warning
2018-12-10 21:27:43.736  INFO 5384 --- [           main] o.s.b.a.w.s.WelcomePageHandlerMapping    : Adding welcome page template: index
2018-12-10 21:27:44.933  INFO 5384 --- [           main] c.darkness.darknessApplicationTests  : Started darknessApplicationTests in 54.632 seconds (JVM running for 73.95)
[INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 61.637 s - in com.darkness.darknessApplicationTests
2018-12-10 21:27:45.631  INFO 5384 --- [       Thread-2] o.s.s.concurrent.ThreadPoolTaskExecutor  : Shutting down ExecutorService 'applicationTaskExecutor'
2018-12-10 21:27:45.634  INFO 5384 --- [       Thread-2] j.LocalContainerEntityManagerFactoryBean : Closing JPA EntityManagerFactory for persistence unit 'default'
2018-12-10 21:27:45.634  INFO 5384 --- [       Thread-2] .SchemaDropperImpl$DelayedDropActionImpl : HHH000477: Starting delayed evictData of schema as part of SessionFactory shut-down'
Hibernate: drop table if exists items
Hibernate: drop table if exists map
Hibernate: drop table if exists msg_cache
Hibernate: drop table if exists npc
Hibernate: drop table if exists users
2018-12-10 21:27:45.750  INFO 5384 --- [       Thread-2] com.zaxxer.hikari.HikariDataSource       : HikariPool-1 - Shutdown initiated...
2018-12-10 21:27:45.806  INFO 5384 --- [       Thread-2] com.zaxxer.hikari.HikariDataSource       : HikariPool-1 - Shutdown completed.
[INFO] 
[INFO] Results:
[INFO] 
[INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0
[INFO] 
[INFO] 
[INFO] --- maven-jar-plugin:3.1.0:jar (default-jar) @ darkness ---
[INFO] Building jar: /home/maestro/git/darkness/target/darkness-.001.jar
[INFO] 
[INFO] --- spring-boot-maven-plugin:2.1.1.RELEASE:repackage (repackage) @ darkness ---
[INFO] Replacing main artifact with repackaged archive
[INFO] 
[INFO] --- maven-install-plugin:2.5.2:install (default-install) @ darkness ---
[INFO] Installing /home/maestro/git/darkness/target/darkness.jar to /home/maestro/.m2/repository/com/run/darkness/.001/darkness-.001.jar
[INFO] Installing /home/maestro/git/darkness/pom.xml to /home/maestro/.m2/repository/com/run/darkness/.001/darkness-.001.pom
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time: 01:35 min
[INFO] Finished at: 2018-12-10T21:27:54-06:00
[INFO] ------------------------------------------------------------------------
-->"# Time Traveling" 
